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

bp = Blueprint("cat", __name__)


@bp.route("/cadastrar-categoria", methods=["GET", "POST"])
def cadastrar_categoria():
    from app.models.categoria import Categoria

    if request.method == "POST":
        nome = request.form["nome"]

        if Categoria.query.filter_by(nome=nome).first():
            flash("Essa categoria já existe.", "warning")
            return redirect(url_for("cat.cadastrar_categoria"))

        nova = Categoria(nome=nome)
        db.session.add(nova)
        db.session.commit()
        flash("Categoria cadastrada com sucesso!", "success")
        return redirect(url_for("cat.cadastro_produto"))

    return render_template("cadastrar_categoria.html")
