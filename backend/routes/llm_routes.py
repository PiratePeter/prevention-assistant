from flask import Blueprint, request
from services.llm_service import get_llm_answer_logic

llm_bp = Blueprint('llm_routes', __name__, url_prefix='/api/regenpreventions')


@llm_bp.route("", methods=["POST"])
def get_llm_answer():
    return get_llm_answer_logic(request)
