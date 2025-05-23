import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.transacao import Transacao
import re

from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("web", __name__)


@bp.route("/home")
def home():
    return redirect(url_for("web.index"))


@bp.route("/")
def index():
    produtos = Produto.query.all()
    if not produtos:
        return render_template("index.html", produtos=[])
    return render_template("produtos.html", produtos=produtos)


@bp.route("/contato")
def contato():
    return render_template("contato.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu com sucesso!", "info")
    return redirect(url_for("web.index"))


@bp.route("/login", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_email"] = usuario.email
            session["usuario_tipo"] = usuario.tipo.value  # comum, trocador, admin
            session["usuario_foto"] = "img/avatar.png"  # futuro campo no model
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("web.index"))
        else:
            flash("Email ou senha incorretos.", "danger")
            return redirect(url_for("web.login_usuario"))

    return render_template("login.html")


@bp.route("/cadastro-usuario", methods=["GET", "POST"])
def cadastro_usuario():
    tipo = request.form.get("tipo", "doador")
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar_senha"]
        cidade = request.form.get("cidade", "")

        if senha != confirmar:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("web.cadastro_usuario"))

        if Usuario.query.filter_by(email=email).first():
            flash("Email já está cadastrado. Tente outro.", "danger")
            return redirect(url_for("web.cadastro_usuario"))

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return redirect(url_for("web.cadastro_usuario"))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("E-mail inválido.", "danger")
            return redirect(url_for("web.cadastro_usuario"))

        if not nome.strip():
            flash("O nome não pode estar vazio.", "danger")
            return redirect(url_for("web.cadastro_usuario"))

        novo = Usuario(nome=nome, email=email, cidade=cidade, tipo=tipo)
        novo.set_senha(senha)

        db.session.add(novo)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("web.login_usuario"))

    return render_template("cadastro_usuario.html")


UPLOAD_FOLDER = os.path.join("app", "static", "uploads")


@bp.route("/cadastro-produto", methods=["GET", "POST"])
def cadastro_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        condicao = request.form["condicao"]
        status = request.form["status"]
        usuario_id = request.form["usuario_id"]
        categoria_id = request.form["categoria_id"]

        foto = request.files["foto"]
        caminho_foto = ""

        if foto and foto.filename != "":
            filename = secure_filename(foto.filename)
            caminho_foto = os.path.join("uploads", filename)
            foto.save(os.path.join("app", "static", caminho_foto))

        produto = Produto(
            nome=nome,
            descricao=descricao,
            condicao=condicao,
            status=status,
            usuario_id=usuario_id,
            categoria_id=categoria_id,
            foto=caminho_foto,
        )

        db.session.add(produto)
        db.session.commit()
        return redirect(url_for("web.index"))

    return render_template("cadastro_produto.html")


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

    return redirect(url_for("web.index"))


@bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


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
