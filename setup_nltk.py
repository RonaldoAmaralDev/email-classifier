"""
Script para baixar os dados necessários do NLTK
Execute este script antes de iniciar a aplicação pela primeira vez
"""

import nltk

def download_nltk_data():
    print("Baixando dados do NLTK...")

    # Tokenizer
    nltk.download('punkt')
    nltk.download('punkt_tab')

    # Stop words
    nltk.download('stopwords')

    # Stemmer para português
    nltk.download('rslp')

    print("Dados do NLTK baixados com sucesso!")

if __name__ == "__main__":
    download_nltk_data()
