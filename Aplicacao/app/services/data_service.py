from app.database import Database
from sqlalchemy import text


class DataService:
    def __init__(self):
        self.db = Database()

    def obter_lotes(self):
        """
        Busca todos os dados da tabela macrocontrole.lote e retorna como um dicionário.
        """
        query = "SELECT id, nome FROM macrocontrole.lote"
        # Transformar em dicionário com o ID como chave
        return {lote["id"]: lote["nome"] for lote in self.db.fetch_all(query)}

    def obter_subfases(self):
        """
        Busca todos os dados da tabela macrocontrole.subfase e retorna como um dicionário.
        """
        query = "SELECT id, nome FROM macrocontrole.subfase"
        # Transformar em dicionário com o ID como chave
        return {subfase["id"]: subfase["nome"] for subfase in self.db.fetch_all(query)}
    
    def listar_materialized_views(self):
        """
        Lista todas as materialized views disponíveis.
        """
        query = """
        SELECT 
            matviewname AS materialized_view
        FROM 
            pg_matviews
        WHERE 
            schemaname = 'acompanhamento';
        """
        return self.db.fetch_all(query)



    def obter_dados_view_especifica(self, view_name):
        """
        Retorna os dados de uma materialized view específica, enriquecendo com os nomes do lote e subfase.
        """
        # Obter nomes de lote e subfase como dicionários
        lotes = self.obter_lotes()
        subfases = self.obter_subfases()

        query = f"""
        SELECT 
            id, lote_id, subfase_id, disponivel, restrito_pre, restrito_exec,
            bloco, nome, dificuldade, tempo_estimado_minutos, dado_producao,
            prioridade, s_1_execucao_usuario, s_1_execucao_data_inicio,
            s_1_execucao_data_fim, s_1_execucao_situacao
        FROM acompanhamento.{view_name};
        """
        dados_view = self.db.fetch_all(query)

        # Enriquecer os dados com os nomes de lote e subfase
        for dado in dados_view:
            dado["lote_nome"] = lotes.get(dado["lote_id"], "Lote Desconhecido")
            dado["subfase_nome"] = subfases.get(dado["subfase_id"], "Subfase Desconhecida")

        return dados_view
    


    def obter_dados_todas_views(self):
        """
        Consulta os dados de todas as materialized views disponíveis no schema.
        """
        # Obter a lista de materialized views
        views = self.listar_materialized_views()

        dados_agrupados = []
        for view in views:
            view_name = view['materialized_view']
            query = f"""
            SELECT 
                id, lote_id, subfase_id, disponivel, restrito_pre, restrito_exec,
                bloco, nome, dificuldade, tempo_estimado_minutos, dado_producao,
                prioridade, s_1_execucao_usuario, s_1_execucao_data_inicio,
                s_1_execucao_data_fim, s_1_execucao_situacao
            FROM acompanhamento.{view_name};
            """
            try:
                dados_view = self.db.fetch_all(query)
                dados_agrupados.append({
                    "view_name": view_name,
                    "data": dados_view
                })
            except Exception as e:
                # Em caso de erro, adicionar um log indicando qual view falhou
                dados_agrupados.append({
                    "view_name": view_name,
                    "error": str(e)
                })
        return dados_agrupados
    
    
    def obter_lotes_subfases(self):
        """
        Busca os lotes e as subfases associadas a cada lote.
        """
        # Obter lotes e subfases como dicionários
        lotes = self.obter_lotes()
        subfases = self.obter_subfases()

        # Buscar materialized views com validação do formato do nome
        query = """
        SELECT DISTINCT 
            matviewname AS materialized_view,
            split_part(matviewname, '_', 2)::INTEGER AS lote_id,
            split_part(matviewname, '_', 4)::INTEGER AS subfase_id
        FROM pg_matviews
        WHERE schemaname = 'acompanhamento'
        AND matviewname SIMILAR TO 'lote_[0-9]+_subfase_[0-9]+';
        """
        relations = self.db.fetch_all(query)

        # Organizar dados por lotes e subfases
        lotes_subfases = {}
        for relation in relations:
            try:
                # Validar se os campos existem e são inteiros
                lote_id = relation.get('lote_id')
                subfase_id = relation.get('subfase_id')
                materialized_view = relation.get('materialized_view')

                if not isinstance(lote_id, int) or not isinstance(subfase_id, int):
                    raise ValueError("IDs inválidos para lote ou subfase.")

                # Adicionar o lote se ainda não estiver registrado
                if lote_id not in lotes_subfases:
                    lote_nome = lotes.get(lote_id, "Lote Desconhecido")
                    lotes_subfases[lote_id] = {
                        "lote_id": lote_id,
                        "lote_nome": lote_nome,
                        "subfases": []
                    }

                # Adicionar a subfase ao lote
                subfase_nome = subfases.get(subfase_id, "Subfase Desconhecida")
                lotes_subfases[lote_id]["subfases"].append({
                    "subfase_id": subfase_id,
                    "subfase_nome": subfase_nome,
                    "materialized_view": materialized_view
                })
            except Exception as e:
                # Logar o erro para depuração
                print(f"Erro ao processar relação: {relation}. Erro: {e}")

        # Retornar os lotes e subfases organizados como uma lista
        return list(lotes_subfases.values())
