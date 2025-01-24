from app.database import Database

class DataService:
    def __init__(self):
        self.db = Database()

    def obter_dados(self):
        """Busca todos os dados da tabela macrocontrole.lote."""
        query = "SELECT * FROM macrocontrole.lote"
        return self.db.fetch_all(query)
    
    def obter_atividades(self, lote_id, subfase_id):
        """
        Busca todas as atividades de um lote e uma subfase específicos.
        """
        query = """
        SELECT 
            a.id AS atividade_id,
            ut.id AS unidade_trabalho_id,
            ut.lote_id,
            ut.subfase_id,
            s.nome AS subfase,
            ts.nome AS situacao,
            a.data_inicio,
            a.data_fim,
            a.observacao
        FROM macrocontrole.atividade a
        JOIN macrocontrole.unidade_trabalho ut ON ut.id = a.unidade_trabalho_id
        JOIN macrocontrole.subfase s ON s.id = ut.subfase_id
        JOIN dominio.tipo_situacao ts ON ts.code = a.tipo_situacao_id
        WHERE ut.lote_id = %s AND ut.subfase_id = %s
        ORDER BY a.id;
        """
        # Executar a consulta com os parâmetros fornecidos
        return self.db.fetch_all(query, (lote_id, subfase_id))
    
    def obter_atividades_agrupadas(self):
        """
        Conta as atividades por status, lote e subfase.
        """
        query = """
        SELECT 
            ut.lote_id,
            ut.subfase_id,
            s.nome AS subfase,
            ts.nome AS situacao,
            COUNT(a.id) AS total_atividades
        FROM macrocontrole.atividade a
        JOIN macrocontrole.unidade_trabalho ut ON ut.id = a.unidade_trabalho_id
        JOIN macrocontrole.subfase s ON s.id = ut.subfase_id
        JOIN dominio.tipo_situacao ts ON ts.code = a.tipo_situacao_id
        GROUP BY ut.lote_id, ut.subfase_id, s.nome, ts.nome
        ORDER BY ut.lote_id, ut.subfase_id, ts.nome;
        """
        return self.db.fetch_all(query)