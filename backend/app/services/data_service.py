from app.database import Database

class DataService:
    def __init__(self):
        self.db = Database()

    def obter_dados(self):
        """Busca todos os dados da tabela macrocontrole.lote."""
        query = "SELECT * FROM macrocontrole.lote"
        return self.db.fetch_all(query)
