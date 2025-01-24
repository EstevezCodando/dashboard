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
def get_dados():
    """Endpoint para buscar os dados do dashboard."""
    try:
        dados = data_service.obter_dados()

        # Retornar a lista diretamente, sem índices numéricos
        return jsonify({"success": True, "data": dados}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@api_bp.route("/api/atividades", methods=["GET"])
def get_atividades():
    """
    Endpoint para buscar todas as atividades de um lote e subfase específicos.
    """
    try:
        # Obter parâmetros da requisição
        lote_id = request.args.get("lote_id", type=int)
        subfase_id = request.args.get("subfase_id", type=int)
        
        # Validar os parâmetros obrigatórios
        if not lote_id or not subfase_id:
            return jsonify({
                "success": False, 
                "error": "Parâmetros 'lote_id' e 'subfase_id' são obrigatórios"
            }), 400

        # Chamar o método com os dois argumentos
        atividades = data_service.obter_atividades(lote_id, subfase_id)

        # Retornar os dados como JSON
        return jsonify({"success": True, "data": atividades}), 200

    except Exception as e:
        # Retornar mensagem de erro em caso de exceção
        return jsonify({"success": False, "error": str(e)}), 500
    
@api_bp.route("/api/atividades/agrupadas", methods=["GET"])
def get_atividades_agrupadas():
    """
    Endpoint para contar as atividades por status, lote e subfase.
    """
    try:
        # Obter os dados agregados
        atividades_agrupadas = data_service.obter_atividades_agrupadas()

        # Retornar os dados como JSON
        return jsonify({"success": True, "data": atividades_agrupadas}), 200

    except Exception as e:
        # Retornar mensagem de erro em caso de exceção
        return jsonify({"success": False, "error": str(e)}), 500