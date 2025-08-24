from flask import Blueprint, request
from services.risk_service import get_risk_evaluation_logic

risk_bp = Blueprint('risk_routes', __name__, url_prefix='/api/risk')


@risk_bp.route("", methods=["POST"])
def get_risk_evaluation():
    return get_risk_evaluation_logic(request)
