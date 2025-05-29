from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect
from config import Config
from flask_login import LoginManager
from flask_login import current_user

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["DEBUG"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_usuario"
    login_manager.session_protection = "strong"
    # Registrar Blueprints
    from app.routes import (
        auth_routes,
        categoria_routes,
        produto_routes,
        transacoes_routes,
        institucional_routes,
        web_routes,
    )

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(produto_routes.bp)
    app.register_blueprint(transacoes_routes.bp)
    app.register_blueprint(institucional_routes.bp)
    app.register_blueprint(web_routes.bp)

    # ✅ Criar administrador padrão após o app e banco estarem prontos
    with app.app_context():
        inspector = inspect(db.engine)
        if inspector.has_table("usuario"):  # confere se a tabela existe
            from app.models.usuario import Usuario, TipoUsuarioEnum
            from app.models.notificacao import Notificacao

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

    @app.context_processor
    def inject_current_user():
        notificacoes_nao_lidas = 0
        if current_user.is_authenticated:
            notificacoes_nao_lidas = Notificacao.query.filter_by(
                usuario_id=current_user.id, lido=False
            ).count()
        return dict(
            current_user=current_user, notificacoes_nao_lidas=notificacoes_nao_lidas
        )

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
