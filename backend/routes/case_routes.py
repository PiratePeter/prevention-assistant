from flask import Blueprint, request
from services.case_service import save_case_logic

case_bp = Blueprint('case_routes', __name__, url_prefix='/api/case')

@case_bp.route("", methods=["POST"])
def save_case():
    return save_case_logic(request)

