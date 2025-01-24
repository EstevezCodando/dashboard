from dash import html, dcc

def criar_layout():
    """Define o layout do Dashboard."""
    return html.Div([
        html.Div([
            # Menu em cascata (Dropdown)
            dcc.Dropdown(
                id='menu-lotes',
                placeholder="Selecione um lote...",
                style={'width': '50%'}
            ),
        ], style={'padding': '10px', 'backgroundColor': '#f9f9f9'}),

        # Gráfico
        dcc.Graph(id='grafico'),

        # Intervalo para atualizações periódicas
        dcc.Interval(
            id='intervalo-atualizacao',
            interval=5000,  # Atualiza a cada 5 segundos
            n_intervals=0
        )
    ])
