from flask import Flask
from flask_talisman import Talisman
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Security
    Talisman(app, force_https=False)  # Disable HTTPS redirect in development

    # Blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
