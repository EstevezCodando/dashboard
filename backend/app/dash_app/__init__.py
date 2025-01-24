from dash import Dash
from app.dash_app.layout import criar_layout
from app.dash_app.callbacks import configurar_callbacks

def criar_dash_app(server):
    """Inicializa o aplicativo Dash."""
    app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
    app.layout = criar_layout()
    configurar_callbacks(app)
    return app
