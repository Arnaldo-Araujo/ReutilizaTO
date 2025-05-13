from flask import Blueprint

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/teste")
def teste():
    return "Blueprint funcionando!"
