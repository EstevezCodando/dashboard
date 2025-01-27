from app import create_app, socketio  # Importa o app Flask e SocketIO
from app.api import api_bp  # Importa as rotas da API
from app.notify import Notifier  # Importa o gerenciador de notificações
from dashFront import init_dash_app  # Importa a função para inicializar o Dash
import threading

def start_notifier():
    """Inicia o gerenciador de notificações do PostgreSQL."""
    notifier = Notifier(socketio)
    notifier.listen_notifications()

if __name__ == "__main__":
    # Cria a aplicação Flask
    app = create_app()

    # Registra as rotas da API
    app.register_blueprint(api_bp)

    # Inicializa o Dash no app Flask
    init_dash_app(app)

    # Inicia o Notifier em uma thread separada
    threading.Thread(target=start_notifier, daemon=True).start()

    # Inicia o servidor Flask com suporte a WebSocket
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
