import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.transacao import Transacao
import re
from uuid import uuid4


from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("instito", __name__)


@bp.route("/contato")
def contato():
    return render_template("contato.html")


@bp.route("/termos-de-uso")
def termos_de_uso():
    return render_template("termos_de_uso.html")


@bp.route("/politica-de-privacidade")
def politica_de_privacidade():
    return render_template("politica_de_privacidade.html")


@bp.route("/sobre")
def sobre():
    return render_template("sobre.html")
