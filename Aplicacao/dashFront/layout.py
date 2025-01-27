from dash import dcc, html

def create_layout():
    """
    Define o layout do Dashboard com boas práticas de UX e design responsivo.
    """
    return html.Div(
        style={
            "backgroundColor": "#121212",  # Cor de fundo mais elegante e moderna
            "color": "black",  # Texto em branco para contraste
            "fontFamily": "Roboto, Arial, sans-serif",
            "padding": "20px",
        },
        children=[
            # Cabeçalho
            html.Header(
                html.H1(
                    "Dashboard de Atividades",
                    style={
                        "textAlign": "center",
                        "padding": "20px 0",
                        "color": "#FF6F61",  # Cor destaque para o título
                        "fontWeight": "bold",
                    },
                )
            ),

            # Dropdown para seleção do lote
            html.Div(
                [
                    html.Label(
                        "Selecione um Lote:",
                        style={
                            "color": "#FF6F61",
                            "fontWeight": "bold",
                            "marginBottom": "10px",
                        },
                    ),
                    dcc.Dropdown(
                        id="lote-dropdown",
                        options=[],  # Preenchido dinamicamente
                        placeholder="Escolha um lote",
                        style={
                            "backgroundColor": "#1F1F1F",
                            "color": "black",
                            "border": "1px solid #FF6F61",
                            "borderRadius": "8px",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "maxWidth": "500px",
                    "margin": "auto",
                    "marginBottom": "20px",
                },
            ),

            # Dropdown para seleção da subfase
            html.Div(
                [
                    html.Label(
                        "Selecione uma Subfase:",
                        style={
                            "color": "black",
                            "fontWeight": "bold",
                            "marginBottom": "10px",
                        },
                    ),
                    dcc.Dropdown(
                        id="subfase-dropdown",
                        options=[],  # Preenchido dinamicamente
                        placeholder="Escolha uma subfase",
                        disabled=True,  # Inicialmente desativado
                        style={
                            "backgroundColor": "#1F1F1F",
                            "color": "black",
                            "border": "1px solid #FF6F61",
                            "borderRadius": "8px",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "maxWidth": "500px",
                    "margin": "auto",
                    "marginBottom": "20px",
                },
            ),

            # Gráficos
            html.Div(
                [
                    html.Div(
                        dcc.Graph(id="progress-pie-chart"),  # Gráfico de Pizza
                        style={"padding": "10px", "flex": "1"},
                    ),
                    html.Div(
                        dcc.Graph(id="user-task-bar-chart"),  # Gráfico de Tarefas por Usuário
                        style={"padding": "10px", "flex": "1"},
                    ),
                    html.Div(
                        dcc.Graph(id="user-time-bar-chart"),  # Gráfico de Tempo Médio por Usuário
                        style={"padding": "10px", "flex": "1"},
                    ),
                    html.Div(
                        dcc.Graph(id="linha_objetivo_feito_e_esperado"),  # Gráfico de Tempo Médio por Usuário
                        style={"padding": "10px", "flex": "1"},
                    ),
                       html.Div(
                        dcc.Graph(id="linha_objetivo_feito_e_esperado_user"),  # Gráfico de Tempo Médio por Usuário
                        style={"padding": "10px", "flex": "1"},
                    ),
                    
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",  # Torna os gráficos responsivos
                    "justifyContent": "center",
                    "gap": "20px",
                    "marginTop": "20px",
                },
            ),

            # Rodapé
            html.Footer(
                "© 2025 Dashboard de Atividades | Desenvolvido por Alvarez",
                style={
                    "textAlign": "center",
                    "paddingTop": "20px",
                    "color": "#888888",
                    "fontSize": "14px",
                },
            ),
        ],
    )
