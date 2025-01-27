from flask import Blueprint, render_template, jsonify, request
from app.services.data_service import DataService


# Inicializar o blueprint
api_bp = Blueprint("api", __name__)

# Instanciar o serviço de dados
data_service = DataService()



@api_bp.route("/", methods=["GET"])
def home():
    """Rota principal para o caminho raiz."""
    return render_template("index.html")

@api_bp.route("/api/lotes", methods=["GET"])
def get_lotes():
    """Endpoint para buscar os dados do dashboard."""
    try:
        dados = data_service.obter_lotes()

        # Retornar a lista diretamente, sem índices numéricos
        return jsonify({"success": True, "data": dados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    


@api_bp.route("/api/subfases", methods=["GET"])
def get_subfases():
    """Endpoint para buscar os dados do dashboard."""
    try:
        dados = data_service.obter_subfases()

        # Retornar a lista diretamente, sem índices numéricos
        return jsonify({"success": True, "data": dados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@api_bp.route("/api/materialized_views", methods=["GET"])
def get_materialized_views():
    """Endpoint para listar todas as materialized views."""
    try:
        materialized_views = data_service.listar_materialized_views()
        return jsonify({"success": True, "data": materialized_views}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    


@api_bp.route("/api/lotes_subfases", methods=["GET"])
def get_lotes_subfases():
    """
    Endpoint para buscar os nomes dos lotes, seus IDs e as subfases associadas.
    """
    try:
        lotes_subfases = data_service.obter_lotes_subfases()
        return jsonify({"success": True, "data": lotes_subfases}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500




@api_bp.route("/api/view/<string:view_name>", methods=["GET"])
def get_view_data(view_name):
    """
    Endpoint para retornar os dados de uma materialized view específica.
    """
    try:
        dados = data_service.obter_dados_view_especifica(view_name)
        return jsonify({"success": True, "data": dados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/api/dados_views", methods=["GET"])
def get_dados_todas_views():
    """
    Endpoint para buscar os dados de todas as materialized views no schema 'acompanhamento'.
    """
    try:
        dados_agrupados = data_service.obter_dados_todas_views()

        return jsonify({"success": True, "data": dados_agrupados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
