import requests
from dash import Input, Output
import plotly.express as px

def configurar_callbacks(app):
    @app.callback(
        Output('menu-lotes', 'options'),
        Input('intervalo-atualizacao', 'n_intervals')
    )
    def atualizar_menu(_):
        """Atualiza o menu em cascata com os nomes dos lotes."""
        try:
            response = requests.get("http://127.0.0.1:5000/api/lotes")
            if response.status_code == 200:
                dados = response.json().get("data", [])
                return [{'label': lote['nome'], 'value': lote['id']} for lote in dados]
        except Exception as e:
            print(f"Erro ao buscar lotes: {e}")
        return []

    @app.callback(
        Output('grafico', 'figure'),
        Input('menu-lotes', 'value')
    )
    def atualizar_grafico(lote_id):
        """Atualiza o gráfico com base no lote selecionado."""
        if not lote_id:
            return px.bar(title="Selecione um lote para visualizar os dados.")
        try:
            response = requests.get(f"http://127.0.0.1:5000/api/lotes")
            if response.status_code == 200:
                dados = response.json().get("data", [])
                dados_filtrados = [d for d in dados if d['id'] == lote_id]
                return px.bar(
                    dados_filtrados,
                    x='descricao',
                    y='denominador_escala',
                    title=f"Dados do Lote {lote_id}"
                )
        except Exception as e:
            print(f"Erro ao buscar dados do lote: {e}")
        return px.bar(title="Erro ao carregar os dados.")
