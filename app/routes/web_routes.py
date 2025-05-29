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

bp = Blueprint("web", __name__)


@bp.route("/home")
def home():
    return redirect(url_for("web.index"))


@bp.route("/campanhas")
def campanhas():
    return render_template("campanhas.html")


@bp.route("/comofunciona")
def comofunciona():
    return render_template("comofunciona.html")
