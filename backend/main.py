"""
Email Classifier API - Backend
Classifica emails em Produtivo/Improdutivo e sugere respostas automáticas
"""

import os
import re
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

# PDF processing
import PyPDF2
import io

# AI API
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Try new google-genai first, fallback to legacy
try:
    from google import genai as google_genai
    USING_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USING_NEW_SDK = False

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp', quiet=True)

# Initialize FastAPI app
app = FastAPI(
    title="Email Classifier API",
    description="API para classificação de emails e sugestão de respostas automáticas",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
gemini_client = None

if GOOGLE_API_KEY:
    if USING_NEW_SDK:
        gemini_client = google_genai.Client(api_key=GOOGLE_API_KEY)
    else:
        genai.configure(api_key=GOOGLE_API_KEY)

# Pydantic models
class EmailInput(BaseModel):
    content: str

class ClassificationResult(BaseModel):
    original_text: str
    processed_text: str
    classification: str
    confidence: float
    suggested_response: str
    keywords: list[str]


class TextProcessor:
    """Classe para processamento de texto com NLP"""

    def __init__(self):
        self.stemmer = RSLPStemmer()
        try:
            self.stop_words = set(stopwords.words('portuguese'))
        except:
            self.stop_words = set()

        # Adicionar stop words em inglês também
        try:
            self.stop_words.update(stopwords.words('english'))
        except:
            pass

    def clean_text(self, text: str) -> str:
        """Remove caracteres especiais e normaliza o texto"""
        # Converter para minúsculas
        text = text.lower()

        # Remover emails
        text = re.sub(r'\S+@\S+', '', text)

        # Remover URLs
        text = re.sub(r'http\S+|www\S+', '', text)

        # Remover caracteres especiais, mantendo acentos
        text = re.sub(r'[^\w\sáéíóúâêîôûãõàèìòùäëïöüç]', ' ', text)

        # Remover números
        text = re.sub(r'\d+', '', text)

        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize(self, text: str) -> list[str]:
        """Tokeniza o texto"""
        return word_tokenize(text, language='portuguese')

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """Remove stop words"""
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]

    def stem_tokens(self, tokens: list[str]) -> list[str]:
        """Aplica stemming nos tokens"""
        return [self.stemmer.stem(token) for token in tokens]

    def process(self, text: str) -> tuple[str, list[str]]:
        """Pipeline completo de processamento"""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        tokens_no_stop = self.remove_stopwords(tokens)
        stemmed = self.stem_tokens(tokens_no_stop)

        return ' '.join(stemmed), tokens_no_stop


class EmailClassifier:
    """Classe para classificação de emails usando IA"""

    def __init__(self):
        self.processor = TextProcessor()
        self.model = None
        self.using_new_sdk = USING_NEW_SDK

        if GOOGLE_API_KEY:
            if USING_NEW_SDK:
                self.model = gemini_client
            else:
                self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Palavras-chave para classificação heurística (fallback)
        self.productive_keywords = [
            'urgente', 'problema', 'erro', 'suporte', 'ajuda', 'dúvida',
            'solicitação', 'requisição', 'pedido', 'atualização', 'status',
            'prazo', 'pendente', 'aguardando', 'necessário', 'importante',
            'bug', 'falha', 'sistema', 'acesso', 'senha', 'relatório',
            'documentação', 'contrato', 'proposta', 'orçamento', 'pagamento',
            'request', 'issue', 'help', 'support', 'update', 'urgent'
        ]

        self.unproductive_keywords = [
            'feliz', 'natal', 'ano novo', 'parabéns', 'aniversário',
            'obrigado', 'agradecimento', 'férias', 'feriado', 'confraternização',
            'boas festas', 'felicitações', 'congratulações', 'sucesso',
            'merry christmas', 'happy', 'birthday', 'thanks', 'thank you',
            'holidays', 'vacation', 'congratulations'
        ]

    def _heuristic_classification(self, text: str, keywords: list[str]) -> tuple[str, float]:
        """Classificação baseada em heurística (fallback quando API não disponível)"""
        text_lower = text.lower()

        productive_score = sum(1 for kw in self.productive_keywords if kw in text_lower)
        unproductive_score = sum(1 for kw in self.unproductive_keywords if kw in text_lower)

        total = productive_score + unproductive_score
        if total == 0:
            # Sem palavras-chave identificadas, assume produtivo por segurança
            return "Produtivo", 0.6

        if productive_score > unproductive_score:
            confidence = min(0.95, 0.6 + (productive_score - unproductive_score) * 0.1)
            return "Produtivo", confidence
        elif unproductive_score > productive_score:
            confidence = min(0.95, 0.6 + (unproductive_score - productive_score) * 0.1)
            return "Improdutivo", confidence
        else:
            return "Produtivo", 0.5

    def _generate_heuristic_response(self, classification: str, text: str) -> str:
        """Gera resposta baseada em templates (fallback)"""
        if classification == "Produtivo":
            return """Prezado(a),

Agradecemos o seu contato. Sua solicitação foi recebida e está sendo analisada pela nossa equipe.

Em breve retornaremos com mais informações sobre o andamento do seu caso.

Caso tenha alguma dúvida adicional, não hesite em nos contatar.

Atenciosamente,
Equipe de Suporte"""
        else:
            return """Prezado(a),

Muito obrigado pela sua mensagem!

Agradecemos o carinho e desejamos o mesmo a você.

Atenciosamente,
Equipe"""

    async def classify_with_ai(self, text: str, processed_text: str, keywords: list[str]) -> tuple[str, float, str]:
        """Classifica email usando Gemini AI"""
        if not self.model:
            classification, confidence = self._heuristic_classification(text, keywords)
            response = self._generate_heuristic_response(classification, text)
            return classification, confidence, response

        prompt = f"""Você é um assistente especializado em classificação de emails corporativos.

Analise o seguinte email e:
1. Classifique como "Produtivo" ou "Improdutivo"
   - Produtivo: emails que requerem ação ou resposta (solicitações, dúvidas, problemas, atualizações de status, etc.)
   - Improdutivo: emails que não necessitam ação (felicitações, agradecimentos, mensagens sociais, etc.)

2. Indique sua confiança na classificação (0.0 a 1.0)

3. Sugira uma resposta automática profissional e adequada em português

EMAIL:
{text}

PALAVRAS-CHAVE IDENTIFICADAS: {', '.join(keywords[:10])}

Responda EXATAMENTE neste formato JSON:
{{
    "classificacao": "Produtivo" ou "Improdutivo",
    "confianca": 0.0 a 1.0,
    "resposta": "texto da resposta sugerida"
}}"""

        try:
            # Generate content based on SDK version
            if self.using_new_sdk:
                response = self.model.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                response_text = response.text.strip()
            else:
                response = self.model.generate_content(prompt)
                response_text = response.text.strip()

            # Extrair JSON da resposta
            import json

            # Tentar encontrar JSON na resposta
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                classification = result.get('classificacao', 'Produtivo')
                confidence = float(result.get('confianca', 0.8))
                suggested_response = result.get('resposta', self._generate_heuristic_response(classification, text))

                return classification, confidence, suggested_response
            else:
                raise ValueError("JSON não encontrado na resposta")

        except Exception as e:
            print(f"Erro na API de IA: {e}")
            # Fallback para classificação heurística
            classification, confidence = self._heuristic_classification(text, keywords)
            response = self._generate_heuristic_response(classification, text)
            return classification, confidence, response

    async def classify(self, text: str) -> ClassificationResult:
        """Pipeline completo de classificação"""
        # Processar texto
        processed_text, keywords = self.processor.process(text)

        # Classificar com IA
        classification, confidence, suggested_response = await self.classify_with_ai(
            text, processed_text, keywords
        )

        return ClassificationResult(
            original_text=text,
            processed_text=processed_text,
            classification=classification,
            confidence=confidence,
            suggested_response=suggested_response,
            keywords=keywords[:15]  # Limitar keywords retornadas
        )


# Inicializar classificador
classifier = EmailClassifier()


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extrai texto de um arquivo PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extrai texto de um arquivo TXT"""
    try:
        # Tentar diferentes encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return file_content.decode(encoding)
            except:
                continue
        raise ValueError("Não foi possível decodificar o arquivo")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo de texto: {str(e)}")


# Get the directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


# API Routes
@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_enabled": bool(GOOGLE_API_KEY),
        "version": "1.0.0"
    }


@app.post("/api/classify/text", response_model=ClassificationResult)
async def classify_text(email_input: EmailInput):
    """Classifica um email a partir de texto direto"""
    if not email_input.content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do email não pode estar vazio")

    return await classifier.classify(email_input.content)


@app.post("/api/classify/file", response_model=ClassificationResult)
async def classify_file(file: UploadFile = File(...)):
    """Classifica um email a partir de arquivo (TXT ou PDF)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo não fornecido")

    # Verificar extensão
    filename_lower = file.filename.lower()
    if not (filename_lower.endswith('.txt') or filename_lower.endswith('.pdf')):
        raise HTTPException(
            status_code=400,
            detail="Formato de arquivo não suportado. Use .txt ou .pdf"
        )

    # Ler conteúdo do arquivo
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio")

    # Extrair texto baseado no tipo de arquivo
    if filename_lower.endswith('.pdf'):
        text = extract_text_from_pdf(content)
    else:
        text = extract_text_from_txt(content)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto do arquivo")

    return await classifier.classify(text)


# Serve static files (frontend)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
