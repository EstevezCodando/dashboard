import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

class Config:
    """Carrega as configurações da aplicação, incluindo as do banco de dados."""
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_default")
    
    # Configurações do Banco de Dados
    DB_CONFIG = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT", "5432"),
    }
