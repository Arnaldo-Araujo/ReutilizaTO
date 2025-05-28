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

bp = Blueprint("trans", __name__)


@bp.route("/historico", methods=["GET"])
def historico_transacoes():
    usuario_id = request.args.get("usuario")
    transacoes = []

    if usuario_id:
        transacoes = (
            Transacao.query.filter(
                (Transacao.de_usuario_id == usuario_id)
                | (Transacao.para_usuario_id == usuario_id)
            )
            .order_by(Transacao.data.desc())
            .all()
        )

    return render_template("historico_transacoes.html", transacoes=transacoes)


@bp.route("/solicitar", methods=["POST"])
def solicitar_produto():
    produto_id = request.form["produto_id"]
    de_usuario_id = request.form["de_usuario_id"]
    para_usuario_id = request.form["para_usuario_id"]
    tipo = request.form["tipo"]

    transacao = Transacao(
        tipo=tipo,
        produto_id=produto_id,
        de_usuario_id=de_usuario_id,
        para_usuario_id=para_usuario_id,
    )

    db.session.add(transacao)

    # Atualiza o status do produto para "reservado"
    produto = Produto.query.get(produto_id)
    produto.status = "reservado"

    db.session.commit()

    return redirect(url_for("trans.index"))
