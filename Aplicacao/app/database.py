import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Config

class Database:
    def __init__(self):
        """Configuração centralizada do banco de dados."""
        self.config = Config.DB_CONFIG

    def connect(self):
        """Cria e retorna uma conexão com o banco de dados."""
        return psycopg2.connect(**self.config)

    def fetch_all(self, query, params=None):
        """Executa uma query e retorna todos os resultados."""
        with self.connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
