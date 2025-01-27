from dash.dependencies import Input, Output
import requests
import dash
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

def register_callbacks(app):
    """
    Registra os callbacks para interatividade do dashboard.
    """

    @app.callback(
    Output("lote-dropdown", "options"),
    Input("lote-dropdown", "value"),
    )
    def load_lotes(_):
        """
        Carrega os lotes do endpoint /api/lotes.
        """
        try:
            response = requests.get("http://127.0.0.1:5000/api/lotes")
            if response.status_code != 200:
                print(f"Erro na resposta da API: {response.status_code}")
                return []
            
            # Converter o JSON retornado
            response_data = response.json()
            lotes_dict = response_data.get("data", {})

            # Verificar se os dados são um dicionário
            if not isinstance(lotes_dict, dict):
                print(f"Formato inesperado: {lotes_dict}")
                return []

            # Transformar o dicionário em uma lista de opções
            return [{"label": nome, "value": int(lote_id)} for lote_id, nome in lotes_dict.items()]

        except Exception as e:
            print(f"Erro ao carregar lotes: {e}")
            return []

    @app.callback(
        [Output("subfase-dropdown", "options"), Output("subfase-dropdown", "disabled")],
        Input("lote-dropdown", "value"),
    )
    def load_subfases(lote_id):
        """
        Carrega as subfases associadas ao lote selecionado.
        """
        if not lote_id:
            # Se nenhum lote foi selecionado, desativar o dropdown
            return [], True

        try:
            # Requisição ao endpoint para obter os lotes e subfases
            response = requests.get("http://127.0.0.1:5000/api/lotes_subfases")
            if response.status_code != 200:
                print(f"Erro na resposta da API: {response.status_code}")
                return [], True

            # Processar os dados retornados
            response_data = response.json()
            lotes_data = response_data.get("data", [])

            # Procurar o lote correspondente ao `lote_id`
            lote = next((l for l in lotes_data if l.get("lote_id") == lote_id), None)
            if lote:
                # Extrair as subfases do lote
                subfases = lote.get("subfases", [])
                options = [{"label": subfase["subfase_nome"], "value": subfase["materialized_view"]} for subfase in subfases]
                return options, False  # Habilitar o dropdown
            else:
                print(f"Lote com ID {lote_id} não encontrado.")
                return [], True  # Nenhum dado encontrado, desativar o dropdown

        except Exception as e:
            print(f"Erro ao carregar subfases: {e}")
            return [], True
        

    @app.callback(
        Output("activity-status-graph", "figure"),
        Input("subfase-dropdown", "value"),
    )
    def update_graph(view_name):
        """
        Atualiza o gráfico com os dados da subfase selecionada.
        """
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]
            status_counts = {}
            for item in data:
                status = item["s_1_execucao_situacao"]
                status_counts[status] = status_counts.get(status, 0) + 1

            figure = {
                "data": [
                    {
                        "x": list(status_counts.keys()),
                        "y": list(status_counts.values()),
                        "type": "bar",
                        "name": "Quantidade de Atividades",
                    }
                ],
                "layout": {
                    "title": "Quantidade de Atividades por Status",
                    "xaxis": {"title": "Status"},
                    "yaxis": {"title": "Quantidade"},
                },
            }
            return figure
        except Exception as e:
            print(f"Erro ao carregar gráfico: {e}")
            return dash.no_update
    @app.callback(
    Output("progress-pie-chart", "figure"),
    Input("subfase-dropdown", "value"),
)
    def update_progress_pie_chart(view_name):
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]

            # Contar os status
            status_counts = {}
            for item in data:
                status = item["s_1_execucao_situacao"]
                status_counts[status] = status_counts.get(status, 0) + 1

            # Criar o gráfico de pizza
            labels = list(status_counts.keys())
            values = list(status_counts.values())

            figure = {
                "data": [
                    {
                        "values": values,
                        "labels": labels,
                        "type": "pie",
                        "hole": 0.4,
                    }
                ],
                "layout": {
                    "title": "% da Subfase Pronta",
                    "paper_bgcolor": "#1e1e1e",
                    "font": {"color": "white"},
                },
            }
            return figure

        except Exception as e:
            print(f"Erro ao carregar gráfico de progresso: {e}")
            return dash.no_update
    @app.callback(
        Output("user-task-bar-chart", "figure"),
        Input("subfase-dropdown", "value"),
    )
    def update_user_task_bar_chart(view_name):
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]

            # Contar as tarefas por usuário
            user_task_counts = {}
            for item in data:
                user = item["s_1_execucao_usuario"] or "Usuário Desconhecido"
                user_task_counts[user] = user_task_counts.get(user, 0) + 1

            # Criar o gráfico de barras
            figure = {
                "data": [
                    {
                        "x": list(user_task_counts.keys()),
                        "y": list(user_task_counts.values()),
                        "type": "bar",
                    }
                ],
                "layout": {
                    "title": "Tarefas Concluídas por Usuário",
                    "xaxis": {"title": "Usuários"},
                    "yaxis": {"title": "Quantidade de Tarefas"},
                    "paper_bgcolor": "#1e1e1e",
                    "font": {"color": "white"},
                },
            }
            return figure

        except Exception as e:
            print(f"Erro ao carregar gráfico de tarefas: {e}")
            return dash.no_update

    @app.callback(
        Output("user-time-bar-chart", "figure"),
        Input("subfase-dropdown", "value"),
    )
    def update_user_time_bar_chart(view_name):
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]

            # Calcular o tempo médio por usuário
            user_times = {}
            for item in data:
                user = item["s_1_execucao_usuario"] or "Usuário Desconhecido"
                start = item["s_1_execucao_data_inicio"]
                end = item["s_1_execucao_data_fim"]

                if start and end:
                    # Converter para datetime
                    start_date = datetime.fromisoformat(start)
                    end_date = datetime.fromisoformat(end)

                    # Calcular diferença descontando finais de semana
                    delta = end_date - start_date
                    total_days = sum(1 for i in range(delta.days + 1)
                                    if (start_date + timedelta(days=i)).weekday() < 5)

                    # Somar ao tempo do usuário
                    user_times[user] = user_times.get(user, []) + [total_days]

            # Calcular a média
            user_avg_times = {user: np.mean(times) for user, times in user_times.items()}

            # Criar o gráfico
            figure = {
                "data": [
                    {
                        "x": list(user_avg_times.keys()),
                        "y": list(user_avg_times.values()),
                        "type": "bar",
                    }
                ],
                "layout": {
                    "title": "Tempo Médio por Usuário (Dias Úteis)",
                    "xaxis": {"title": "Usuários"},
                    "yaxis": {"title": "Tempo Médio (dias)"},
                    "paper_bgcolor": "#1e1e1e",
                    "font": {"color": "white"},
                },
            }
            return figure

        except Exception as e:
            print(f"Erro ao carregar gráfico de tempo médio: {e}")
            return dash.no_update
    @app.callback(
        Output("linha_objetivo_feito_e_esperado", "figure"),
        Input("subfase-dropdown", "value"),
    )
    def linha_objetivo_feito_e_esperado(view_name):
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]

            # Obter a data mais antiga das atividades
            datas_inicio = [
                datetime.fromisoformat(item["s_1_execucao_data_inicio"][:19])
                for item in data
                if item["s_1_execucao_data_inicio"] is not None
            ]
            data_inicio = min(datas_inicio)

            # Contar o número total de atividades
            total_atividades = len(data)

            # Configuração do número de operadores ao longo do tempo
            configuracao_operadores = [
                (16, 2),  # Dias 1 a 5: 2 operadores
            ]

            # Progresso esperado
            dias_uteis = []
            progresso_esperado = []
            atividades_concluidas = 0
            dia_atual = data_inicio
            print(dia_atual)
            total_dias = 0

            for duracao, operadores in configuracao_operadores:
                for _ in range(duracao):
                    if atividades_concluidas >= total_atividades:
                        break
                    dias_uteis.append(dia_atual)
                    produtividade_diaria = operadores  # Assume 1 atividade por operador/dia
                    atividades_concluidas += produtividade_diaria
                    progresso_esperado.append(min(atividades_concluidas, total_atividades))
                    dia_atual += timedelta(days=1)
                    while dia_atual.weekday() >= 5:  # Pular finais de semana
                        dia_atual += timedelta(days=1)
                    total_dias += 1

            # Progresso real
            progresso_real = defaultdict(int)

            # Iterar sobre as atividades para calcular progresso real
            for item in data:
                status = item["s_1_execucao_situacao"]
                data_fim = item.get("s_1_execucao_data_fim")

                # Depurar itens relevantes
                print(f"Atividade: {item['nome']}, Status: {status}, Data Fim: {data_fim}")

                if status == "Finalizada" and data_fim:
                    try:
                        # Converter para datetime.date
                        data_fim_date = datetime.fromisoformat(data_fim[:19]).date()
                        progresso_real[data_fim_date] += 1
                    except Exception as e:
                        print(f"Erro ao processar a data {data_fim}: {e}")

            # Verificar progresso real acumulado
            progresso_real_acumulado = []
            atividades_realizadas = 0
            ultimo_dia_real = None

            for dia in dias_uteis:
                dia_date = dia.date()  # Garantir que o dia também é um objeto datetime.date
                atividades_realizadas += progresso_real[dia_date]
                progresso_real_acumulado.append(atividades_realizadas)
                if progresso_real[dia_date] > 0:
                    ultimo_dia_real = dia
                print(f"Dia: {dia_date}, Atividades Realizadas: {atividades_realizadas}, Progresso Real: {progresso_real[dia_date]}")

            # Ajustar progresso real para mostrar apenas até o último dia com atividades concluídas
            if ultimo_dia_real:
                indice_ultimo_dia = dias_uteis.index(ultimo_dia_real)
                progresso_real_acumulado = progresso_real_acumulado[:indice_ultimo_dia + 1]
                dias_uteis_real = dias_uteis[:indice_ultimo_dia + 1]
            else:
                dias_uteis_real = []

            # Construção do gráfico
            figura = {
                "data": [
                    {
                        "x": dias_uteis,
                        "y": progresso_esperado,
                        "type": "line",
                        "name": "Progresso Esperado",
                    },
                    {
                        "x": dias_uteis_real,
                        "y": progresso_real_acumulado,
                        "type": "line",
                        "name": "Progresso Real",
                    },
                ],
                "layout": {
                    "title": "Previsão vs Realidade de Conclusão de Atividades",
                    "xaxis": {"title": "Dias Úteis"},
                    "yaxis": {"title": "Número de Atividades Concluídas"},
                    "paper_bgcolor": "#1e1e1e",
                    "font": {"color": "white"},
                    "legend": {
                        "title": "Legenda",
                        "items": [
                            {
                                "name": f"Progresso Real (Última data: {ultimo_dia_real.strftime('%b %d') if ultimo_dia_real else 'N/A'}, Qtd de Atividades: {atividades_realizadas})"
                            },
                        ]
                    },
                },
            }

            return figura

        except Exception as e:
            print(f"Erro ao carregar gráfico de previsão dinâmica: {e}")
            return dash.no_update

    @app.callback(
        Output("linha_objetivo_feito_e_esperado_user", "figure"),
        Input("subfase-dropdown", "value"),
    )
    def linha_objetivo_feito_e_esperado_user(view_name):
        if not view_name:
            return dash.no_update

        try:
            response = requests.get(f"http://127.0.0.1:5000/api/view/{view_name}")
            data = response.json()["data"]

            # Organizar as atividades por usuário
            atividades_por_usuario = defaultdict(list)
            for item in data:
                usuario = item.get("s_1_execucao_usuario", "Desconhecido")
                atividades_por_usuario[usuario].append(item)

            # Construir o gráfico por usuário
            traces = []
            for usuario, atividades in atividades_por_usuario.items():
                # Obter a data mais antiga de início do usuário
                datas_inicio = [
                    datetime.fromisoformat(item["s_1_execucao_data_inicio"][:19])
                    for item in atividades
                    if item["s_1_execucao_data_inicio"] is not None
                ]
                if not datas_inicio:
                    continue

                data_inicio = min(datas_inicio)
                data_fim = datetime.now()

                # Gerar lista de dias úteis entre a data de início e hoje
                dias_uteis = []
                dia_atual = data_inicio
                while dia_atual.date() <= data_fim.date():
                    if dia_atual.weekday() < 5:  # Dias úteis apenas
                        dias_uteis.append(dia_atual)
                    dia_atual += timedelta(days=1)

                # Progresso esperado (1 atividade por dia útil)
                progresso_esperado = list(range(1, len(dias_uteis) + 1))

                # Progresso real
                progresso_real = defaultdict(int)
                for item in atividades:
                    status = item["s_1_execucao_situacao"]
                    data_fim = item.get("s_1_execucao_data_fim")

                    if status == "Finalizada" and data_fim:
                        try:
                            data_fim_date = datetime.fromisoformat(data_fim[:19]).date()
                            progresso_real[data_fim_date] += 1
                        except Exception as e:
                            print(f"Erro ao processar a data {data_fim}: {e}")

                progresso_real_acumulado = []
                atividades_realizadas = 0
                for dia in dias_uteis:
                    dia_date = dia.date()
                    atividades_realizadas += progresso_real[dia_date]
                    progresso_real_acumulado.append(atividades_realizadas)

                # Adicionar trace para o usuário
                traces.append({
                    "x": [dia.strftime('%b %d, %Y') for dia in dias_uteis],
                    "y": progresso_esperado,
                    "type": "line",
                    "name": f"Progresso Esperado ({usuario})",
                })
                traces.append({
                    "x": [dia.strftime('%b %d, %Y') for dia in dias_uteis],
                    "y": progresso_real_acumulado,
                    "type": "line",
                    "name": f"Progresso Real ({usuario})",
                })

            # Construção do gráfico
            figura = {
                "data": traces,
                "layout": {
                    "title": "Previsão vs Realidade de Conclusão de Atividades por Usuário",
                    "xaxis": {"title": "Dias Úteis"},
                    "yaxis": {"title": "Número de Atividades Concluídas"},
                    "paper_bgcolor": "#1e1e1e",
                    "font": {"color": "white"},
                },
            }

            return figura

        except Exception as e:
            print(f"Erro ao carregar gráfico de previsão dinâmica: {e}")
            return dash.no_update
