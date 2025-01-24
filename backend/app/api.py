from flask import Blueprint, render_template, jsonify
from app.services.data_service import DataService

# Criar o blueprint para rotas
api_bp = Blueprint("api", __name__)
data_service = DataService()

@api_bp.route("/", methods=["GET"])
def home():
    """Rota principal para o caminho raiz."""
    return render_template("index.html")

@api_bp.route("/api/lotes", methods=["GET"])
def get_dados():
    """Endpoint para buscar os dados do dashboard."""
    try:
        dados = data_service.obter_dados()

        # Retornar a lista diretamente, sem índices numéricos
        return jsonify({"success": True, "data": dados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500