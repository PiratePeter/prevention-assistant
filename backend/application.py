from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()
from routes.case_routes import case_bp, cases_bp
from routes.llm_routes import llm_bp
from routes.recommendation_routes import recommendation_bp
from routes.risk_routes import risk_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(llm_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(cases_bp)

    @app.route("/")
    def index():
        return "API is running"

    return app

application = create_app() # NOTE: Needed for AWS Elastic Beanstalk

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    application.run(debug=True, host="0.0.0.0", port=5000)
