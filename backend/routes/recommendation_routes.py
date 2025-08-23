from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas.recommendation_schema import DamageReportSchema
from services.recommendation_service import gen_recommendation_logic
import logging

# Define the blueprint for the questionnaire routes
recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/api')
schema = DamageReportSchema()

# Configure logging
logging.basicConfig(level=logging.INFO)

@recommendation_bp.route("/recommendation", methods=["POST"])
def gen_recommendation():
    """
    Endpoint to generate a recommendation based on the damage report.
    Expects a JSON payload with damage details, building information, and specific questions.
    :return: JSON response with generated recommendation or error message.
    """
    try:
        # 1. Validate input
        data = schema.load(request.get_json())

        # 2. Call service with clean data
        report = gen_recommendation_logic(data)

        # 3: Combine the recommendation with the original data
        data['preventions'] = report['recommendation']

        # 4. Return response
        return jsonify(schema.dump(data)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
