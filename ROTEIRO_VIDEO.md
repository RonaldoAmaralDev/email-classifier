# Roteiro do Vídeo Demonstrativo - Email Classifier

**Duração Total:** 3-5 minutos

---

## 1. INTRODUÇÃO (30 segundos)

**[Aparecer na tela ou narrar]**

> "Olá! Meu nome é Ronaldo Amaral e vou apresentar o Email Classifier, uma solução que desenvolvi para o desafio da AutoU."

> "O objetivo é automatizar a classificação de emails em uma empresa do setor financeiro, categorizando-os como Produtivos ou Improdutivos e sugerindo respostas automáticas."

---

## 2. DEMONSTRAÇÃO DA APLICAÇÃO (3 minutos)

### 2.1 Apresentar a Interface (30 segundos)

**[Mostrar a tela inicial: https://email-classifier-dutw.onrender.com]**

> "Esta é a interface da aplicação. Temos duas formas de entrada: digitar o texto diretamente ou fazer upload de um arquivo PDF ou TXT."

> "No canto esquerdo vemos o indicador de status mostrando que a IA está conectada."

---

### 2.2 Testar Email PRODUTIVO (1 minuto)

**[Clicar no botão "Suporte Técnico" nos exemplos rápidos]**

> "Vou começar testando um email de suporte técnico - um caso típico de email produtivo que requer ação."

**[Clicar em "Classificar Email"]**

> "A aplicação processou o texto usando técnicas de NLP e enviou para a API do Google Gemini."

**[Mostrar o resultado]**

> "Vejam o resultado:
> - Classificação: **Produtivo** - correto, pois é uma solicitação de suporte
> - Confiança: **alta** - a IA tem certeza da classificação
> - Resposta sugerida: uma resposta profissional e adequada
> - Palavras-chave identificadas: suporte, problema, sistema, urgente..."

**[Clicar em "Copiar Resposta"]**

> "Posso copiar a resposta sugerida diretamente para usar no email."

---

### 2.3 Testar Email IMPRODUTIVO (1 minuto)

**[Clicar em "Nova Classificação" e depois em "Feliz Natal"]**

> "Agora vou testar um email improdutivo - uma mensagem de felicitações de Natal."

**[Clicar em "Classificar Email"]**

> "Vejam que a classificação mudou:
> - Classificação: **Improdutivo** - correto, é uma mensagem social
> - A resposta sugerida é mais curta e adequada ao contexto
> - Palavras-chave: feliz, natal, ano novo, boas festas..."

---

### 2.4 Testar Upload de Arquivo (30 segundos)

**[Clicar na aba "Upload Arquivo"]**

> "Também é possível fazer upload de arquivos. A aplicação aceita TXT e PDF."

**[Arrastar ou selecionar um arquivo de exemplo]**

> "O sistema extrai o texto automaticamente e faz a classificação."

---

## 3. EXPLICAÇÃO TÉCNICA (1 minuto)

**[Pode mostrar o código ou diagrama]**

> "Sobre a arquitetura técnica:"

> "**Backend:** Desenvolvido em Python com FastAPI, um framework moderno e de alta performance."

> "**Processamento NLP:** Utilizo a biblioteca NLTK para:
> - Tokenização do texto
> - Remoção de stopwords em português e inglês
> - Stemming com o algoritmo RSLP para português"

> "**Classificação com IA:** Integração com a API do Google Gemini. Envio um prompt estruturado e recebo a classificação, confiança e resposta sugerida em formato JSON."

> "**Fallback:** Caso a API esteja indisponível, o sistema usa classificação heurística baseada em palavras-chave."

> "**Frontend:** HTML, CSS e JavaScript separados, com design responsivo e acessível."

> "**Deploy:** Hospedado no Render com configuração automática via render.yaml."

---

## 4. CONCLUSÃO (30 segundos)

> "Em resumo, o Email Classifier automatiza a triagem de emails, economizando tempo da equipe ao:
> - Identificar rapidamente emails que precisam de ação
> - Sugerir respostas prontas para agilizar o atendimento
> - Processar arquivos PDF e TXT automaticamente"

> "O código está disponível no GitHub e a aplicação está online no Render."

> "Obrigado pela atenção!"

---