from flask import Flask
from flask_socketio import SocketIO
from app.dash_app import criar_dash_app
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurar SocketIO
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    """Cria a aplicação Flask e integra o Dash."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_default')
    
    # Inicializar o Dash e vinculá-lo ao app Flask
    criar_dash_app(app)

    return app
