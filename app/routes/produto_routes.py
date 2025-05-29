import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import usuario
from app.models.usuario import TipoUsuarioEnum, Usuario
from app.models.produto import Produto
from app.models.transacao import Transacao
from flask_wtf import FlaskForm
from wtforms import HiddenField
import re
from uuid import uuid4


from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("prod", __name__)


class DummyForm(FlaskForm):
    dummy = HiddenField()


@bp.route("/")
def index():
    produtos = Produto.query.filter_by(aprovado=True).all()
    if not produtos:
        return render_template("index.html", produtos=[])
    return render_template("produtos.html", produtos=produtos)


@bp.route("/cadastro-produto", methods=["GET", "POST"])
@login_required
def cadastro_produto():
    from app.models.categoria import Categoria
    from app.models.produto import Produto
    from app.models.foto_produto import FotoProduto

    if request.method == "POST":
        try:
            nome = request.form.get("nome")
            descricao = request.form.get("descricao")
            condicao = request.form.get("condicao")
            status = request.form.get("status")
            usuario_id = request.form.get("usuario_id")
            categoria_id = request.form.get("categoria_id")
            fotos = request.files.getlist("fotos")
            novo_produto = db.Column(db.Boolean, default=False)

            print("DADOS RECEBIDOS:")
            print("nome:", nome)
            print("usuario_id:", usuario_id)
            print("qtd fotos:", len(fotos))

            if not nome or not usuario_id or not categoria_id:
                return "Campos obrigatórios não preenchidos", 400

            produto = Produto(
                nome=nome,
                descricao=descricao,
                condicao=condicao,
                status=status,
                usuario_id=usuario_id,
                categoria_id=categoria_id,
            )
            db.session.add(produto)
            db.session.commit()

            for foto in fotos:
                if foto and foto.filename:
                    filename = secure_filename(f"{uuid4().hex}_{foto.filename}")
                    caminho = f"uploads/{filename}"  # 🔥 Isso evita o problema de barra invertida
                    foto.save(os.path.join("app", "static", "uploads", filename))

                    nova_foto = FotoProduto(caminho=caminho, produto_id=produto.id)
                    db.session.add(nova_foto)

            db.session.commit()
            flash("Produto cadastrado com sucesso!", "success")
            return redirect(url_for("prod.index"))

        except Exception as e:
            print("Erro ao processar POST /cadastro-produto:", e)
            return "Erro interno no servidor", 500

    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    return render_template("cadastro_produto.html", categorias=categorias)


@bp.route("/excluir-produto/<int:produto_id>", methods=["POST"])
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if (
        session.get("usuario_id") != produto.usuario_id
        and session.get("usuario_tipo") != "administrador"
    ):
        flash("Você não tem permissão para excluir este produto.", "danger")
        return redirect(url_for("prod.index"))

    # Remove as fotos (e arquivos físicos, se quiser)
    for foto in produto.fotos:
        caminho_fisico = os.path.join("app", "static", foto.caminho)
        if os.path.exists(caminho_fisico):
            os.remove(caminho_fisico)
        db.session.delete(foto)

    db.session.delete(produto)
    db.session.commit()

    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for("prod.index"))


@bp.route("/aprovar")
def aprovar():
    if not session.get("usuario_id"):
        flash("Você precisa estar logado.", "warning")
        return redirect(url_for("auth.login_usuario"))

    usuario = Usuario.query.get(session["usuario_id"])

    if not usuario or usuario.tipo not in [
        TipoUsuarioEnum.administrador,
        TipoUsuarioEnum.moderador,
    ]:
        flash("Acesso não autorizado", "danger")
        return redirect(url_for("prod.index"))

    produtos_pendentes = Produto.query.filter(
        or_(Produto.aprovado == False, Produto.aprovado.is_(None))
    ).all()
    return render_template("produtos_aprovar.html", produtos=produtos_pendentes)


@bp.route("/aprovar/<int:id>", methods=["POST"])
def aprovar_produto(id):
    if session.get("usuario_tipo") != "administrador":
        flash("Acesso não autorizado", "danger")
        return redirect(url_for("prod.index"))
    produto = Produto.query.get_or_404(id)
    produto.aprovado = True
    db.session.commit()
    flash("Produto aprovado com sucesso!", "success")
    return redirect(url_for("prod.aprovar"))


@bp.route("/produto/<int:id>/reprovar", methods=["POST"])
def reprovar_produto(id):
    produto = Produto.query.get_or_404(id)

    if session.get("usuario_tipo") != "administrador":
        flash("Você não tem permissão para excluir este produto.", "danger")
        return redirect(url_for("prod.index"))

    # Remove as fotos (e arquivos físicos, se quiser)
    for foto in produto.fotos:
        caminho_fisico = os.path.join("app", "static", foto.caminho)
        if os.path.exists(caminho_fisico):
            os.remove(caminho_fisico)
        db.session.delete(foto)

    db.session.delete(produto)
    db.session.commit()

    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for("prod.index"))
