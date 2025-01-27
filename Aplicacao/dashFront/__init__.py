from dash import Dash
from flask import Flask
from dashFront.layout import create_layout
from dashFront.callbacks import register_callbacks

def init_dash_app(server: Flask):
    """
    Inicializa o Dash como um módulo dentro do app Flask.
    """
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',  # Base URL para o Dash
    )
    dash_app.title = "Dashboard de Atividades"
    
    # Configurar layout
    dash_app.layout = create_layout()
    
    # Registrar callbacks
    register_callbacks(dash_app)
    
    return dash_app
