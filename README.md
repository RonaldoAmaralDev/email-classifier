# Email Classifier - Classificação Inteligente de Emails

Sistema de classificação automática de emails utilizando Inteligência Artificial para categorizar mensagens como **Produtivas** ou **Improdutivas** e sugerir respostas automáticas.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Demonstração

🌐 **Aplicação Online:** [Link da aplicação deployada]

📹 **Vídeo Demonstrativo:** [Link do YouTube]

## Funcionalidades

- **Classificação de Emails:** Categoriza emails em Produtivo ou Improdutivo
- **Sugestão de Respostas:** Gera respostas automáticas adequadas ao contexto
- **Upload de Arquivos:** Suporta arquivos .txt e .pdf
- **Entrada de Texto:** Permite colar ou digitar o conteúdo diretamente
- **Processamento NLP:** Utiliza técnicas de processamento de linguagem natural
- **Interface Responsiva:** Design moderno e intuitivo

## Categorias de Classificação

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| **Produtivo** | Emails que requerem ação ou resposta | Solicitações de suporte, dúvidas técnicas, atualizações de status, pedidos de informação |
| **Improdutivo** | Emails que não necessitam ação imediata | Mensagens de felicitações, agradecimentos, comunicados sociais |

## Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e de alta performance
- **NLTK** - Processamento de linguagem natural (tokenização, stemming, stop words)
- **PyPDF2** - Extração de texto de arquivos PDF
- **Google Gemini AI** - API de IA para classificação e geração de respostas

### Frontend
- **HTML5/CSS3** - Interface web responsiva
- **JavaScript (Vanilla)** - Interatividade e comunicação com API
- **Font Awesome** - Ícones

### Deploy
- **Render/Railway/Heroku** - Hospedagem em nuvem
- **Gunicorn + Uvicorn** - Servidor de produção

## Estrutura do Projeto

```
email-classifier/
├── backend/
│   └── main.py                 # API FastAPI principal
├── frontend/
│   ├── index.html              # Página principal HTML
│   ├── css/
│   │   └── styles.css          # Estilos CSS separados
│   └── js/
│       └── app.js              # JavaScript da aplicação
├── samples/
│   ├── email_suporte.txt       # Exemplo de email produtivo
│   ├── email_status.txt        # Exemplo de email produtivo
│   ├── email_natal.txt         # Exemplo de email improdutivo
│   └── email_agradecimento.txt # Exemplo de email improdutivo
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore
├── LICENSE                     # Licença MIT
├── Procfile                    # Configuração para Heroku
├── render.yaml                 # Configuração para Render
├── runtime.txt                 # Versão do Python
├── requirements.txt            # Dependências Python
├── setup_nltk.py               # Script para setup do NLTK
└── README.md
```

## Instalação e Execução Local

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/email-classifier.git
cd email-classifier
```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Baixe os dados do NLTK:**
```bash
python setup_nltk.py
```

5. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua chave da API do Google Gemini
```

6. **Execute a aplicação:**
```bash
cd backend
python main.py
```

7. **Acesse a aplicação:**
   Abra o navegador em `http://localhost:8000`

## Configuração da API de IA

### Google Gemini (Recomendado)

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave de API
3. Adicione a chave no arquivo `.env`:
```
GOOGLE_API_KEY=sua_chave_aqui
```

> **Nota:** A aplicação funciona mesmo sem a chave de API, utilizando um sistema de classificação heurística como fallback.

## API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Serve a interface web |
| `GET` | `/docs` | Documentação interativa (Swagger) |
| `GET` | `/health` | Health check da API |
| `POST` | `/api/classify/text` | Classifica email por texto |
| `POST` | `/api/classify/file` | Classifica email por arquivo |

> **Dica:** Acesse `http://localhost:8000/docs` para testar a API interativamente via Swagger UI.

### Exemplo de Requisição

```bash
curl -X POST "http://localhost:8000/api/classify/text" \
  -H "Content-Type: application/json" \
  -d '{"content": "Prezado suporte, estou com problemas no sistema..."}'
```

### Exemplo de Resposta

```json
{
  "original_text": "Prezado suporte, estou com problemas no sistema...",
  "processed_text": "prezad suport problem sistem",
  "classification": "Produtivo",
  "confidence": 0.92,
  "suggested_response": "Prezado(a),\n\nAgradecemos o seu contato...",
  "keywords": ["suporte", "problema", "sistema"]
}
```

## Deploy em Produção

### Render

1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente (GOOGLE_API_KEY)
3. O deploy será automático usando o `render.yaml`

### Railway

1. Importe o projeto do GitHub
2. Adicione a variável de ambiente GOOGLE_API_KEY
3. Deploy automático

### Heroku

```bash
heroku create nome-do-app
heroku config:set GOOGLE_API_KEY=sua_chave
git push heroku main
```

## Arquitetura do Sistema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   Backend       │────▶│   Gemini AI     │
│   (HTML/JS)     │     │   (FastAPI)     │     │   (Google)      │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │                 │
                        │   NLP Pipeline  │
                        │   (NLTK)        │
                        │                 │
                        └─────────────────┘
```

### Fluxo de Processamento

1. **Entrada:** Usuário envia email (texto ou arquivo)
2. **Pré-processamento NLP:**
   - Limpeza do texto (remoção de URLs, emails, caracteres especiais)
   - Tokenização
   - Remoção de stop words (português e inglês)
   - Stemming (RSLPStemmer para português)
3. **Classificação com IA:**
   - Envio para API Gemini com prompt estruturado
   - Fallback para classificação heurística se API indisponível
4. **Geração de Resposta:**
   - IA gera resposta contextualizada
   - Template de resposta como fallback
5. **Retorno:** Resultado com classificação, confiança e resposta sugerida

## Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Desenvolvido para o Desafio AutoU - Classificação Inteligente de Emails

---

**Nota:** Este projeto foi desenvolvido como parte de um desafio técnico e demonstra a aplicação de técnicas de NLP e IA para automatização de processos empresariais.
