from flask import Blueprint, request
from services.case_service import (load_case_logic, load_cases_logic,
                                   save_case_logic)

case_bp = Blueprint('case_routes', __name__, url_prefix='/api/case')
cases_bp = Blueprint('cases_routes', __name__, url_prefix='/api/cases')

@case_bp.route("", methods=["POST"])
def save_case():
    return save_case_logic(request)

@case_bp.route("", methods=["GET"])
def load_case():
    return load_case_logic(request)

@cases_bp.route("", methods=["GET"])
def load_cases():
    return load_cases_logic(request)

