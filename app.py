import warnings
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=UserWarning)

from config import Config
from src.models.db import db, User
from src.routes.main import main_bp
from src.routes.api import api_bp
from src.routes.auth import auth_bp, oauth

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    # Auth
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Initialize OAuth with app
    oauth.init_app(app)

    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
import os

port = int(os.environ.get("PORT", 5000))  # Render sets PORT dynamically
app.run(host="0.0.0.0", port=port)