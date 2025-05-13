from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def index():
        return "Sistema ReutilizaTO rodando com sucesso!"

    return app
