import os
from werkzeug.utils import secure_filename
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask_login import current_user, login_required, LoginManager, login_user
from app import db
from app.models.usuario import TipoUsuarioEnum, Usuario
import re
from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu com sucesso!", "info")
    return redirect(url_for("prod.index"))


@bp.route("/login", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)  # 👈 ESSENCIAL
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_email"] = usuario.email
            session["usuario_tipo"] = usuario.tipo.value
            session["usuario_foto"] = "img/avatar.png"
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("prod.index"))
        else:
            flash("Email ou senha incorretos.", "danger")
            return redirect(url_for("auth.login_usuario"))

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
            return redirect(url_for("auth.cadastro_usuario"))

        if Usuario.query.filter_by(email=email).first():
            flash("Email já está cadastrado. Tente outro.", "danger")
            return redirect(url_for("auth.cadastro_usuario"))

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return redirect(url_for("auth.cadastro_usuario"))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("E-mail inválido.", "danger")
            return redirect(url_for("auth.cadastro_usuario"))

        if not nome.strip():
            flash("O nome não pode estar vazio.", "danger")
            return redirect(url_for("auth.cadastro_usuario"))

        novo = Usuario(nome=nome, email=email, cidade=cidade, tipo=tipo)
        novo.set_senha(senha)

        db.session.add(novo)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("auth.login_usuario"))

    return render_template("cadastro_usuario.html")


UPLOAD_FOLDER = os.path.join("app", "static", "uploads")


@bp.route("/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario_alvo = Usuario.query.get_or_404(id)
    usuario_atual = Usuario.query.get(session["usuario_id"])

    dados = request.get_json()

    # Somente administradores podem alterar o tipo
    novo_tipo = dados.get("tipo")
    if novo_tipo and current_user.tipo != TipoUsuarioEnum.administrador:
        return (
            jsonify(
                {"erro": "Apenas administradores podem alterar o tipo de usuário."}
            ),
            403,
        )

    usuario_alvo.nome = dados.get("nome", usuario_alvo.nome)
    usuario_alvo.cidade = dados.get("cidade", usuario_alvo.cidade)

    if novo_tipo and current_user.tipo == TipoUsuarioEnum.administrador:
        usuario_alvo.tipo = novo_tipo

    db.session.commit()
    return jsonify(usuario_alvo.to_dict())


@bp.route("/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    usuario_alvo = Usuario.query.get_or_404(id)
    usuario_atual = Usuario.query.get(session["usuario_id"])

    # Verifica se o atual é administrador
    if current_user.tipo != TipoUsuarioEnum.administrador:
        return jsonify({"erro": "Apenas administradores podem excluir usuários."}), 403

    db.session.delete(usuario_alvo)
    db.session.commit()
    return jsonify({"mensagem": "Usuário excluído com sucesso"})


@bp.route("/gerenciar", methods=["GET"])
@login_required
def gerenciar():
    if current_user.tipo != TipoUsuarioEnum.administrador:
        flash("Acesso negado.", "danger")
        return redirect(url_for("web.index"))

    usuarios = Usuario.query.all()
    return render_template("admin/gerenciar_usuarios.html", usuarios=usuarios)
