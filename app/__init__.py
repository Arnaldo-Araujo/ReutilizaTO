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

    # Registrar Blueprints
    from app.routes import (
        usuario_routes,
        categoria_routes,
        produto_routes,
        transacao_routes,
        web_routes,
    )

    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(produto_routes.bp)
    app.register_blueprint(transacao_routes.bp)
    app.register_blueprint(web_routes.bp)

    # ✅ Criar administrador padrão após o app e banco estarem prontos
    with app.app_context():
        from app.models.usuario import Usuario, TipoUsuarioEnum

        if not Usuario.query.filter_by(email="admin@reutilizato.org").first():
            admin = Usuario(
                nome="Administrador",
                email="admin@reutilizato.org",
                tipo=TipoUsuarioEnum.administrador,
            )
            admin.set_senha("admin!@#")
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário administrador criado!")

    return app
