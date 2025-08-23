from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()
from routes.llm_routes import llm_bp
from routes.risk_routes import risk_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(llm_bp)
    app.register_blueprint(risk_bp)

    @app.route("/")
    def index():
        return "API is running"

    return app


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    flask_app = create_app()
    flask_app.run(debug=True, host="0.0.0.0", port=5000)
