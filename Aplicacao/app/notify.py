import psycopg2
from app.config import Config

class Notifier:
    def __init__(self, socketio):
        """Configuração centralizada do banco de dados."""
        self.socketio = socketio
        self.config = Config.DB_CONFIG

    def listen_notifications(self, channel="atualizacao_tabela"):
        """Escuta notificações no canal do PostgreSQL."""
        with psycopg2.connect(**self.config) as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f"LISTEN {channel};")
            print(f"Aguardando notificações no canal '{channel}'...")

            while True:
                conn.poll()
                while conn.notifies:
                    notificacao = conn.notifies.pop(0)
                    self.socketio.emit("atualizacao", {"data": notificacao.payload})
