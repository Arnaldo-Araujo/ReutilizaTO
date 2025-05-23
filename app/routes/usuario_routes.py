from flask import Blueprint, request, jsonify
from app import db
from app.models.usuario import Usuario

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


# Listar usuários
@bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


# Cadastrar usuário
@bp.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():
    dados = request.get_json()
    if Usuario.query.filter_by(email=dados["email"]).first():
        return jsonify({"erro": "Email já cadastrado"}), 400

    usuario = Usuario(
        nome=dados["nome"],
        email=dados["email"],
        cidade=dados.get("cidade", ""),
        tipo=dados.get("tipo", "comum"),
    )
    usuario.set_senha(dados["senha"])

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.to_dict()), 201


# Login de usuário
@bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados["email"]).first()

    if usuario and usuario.verificar_senha(dados["senha"]):
        return jsonify({"mensagem": "Login bem-sucedido", "usuario": usuario.to_dict()})
    return jsonify({"erro": "Credenciais inválidas"}), 401


# Atualizar usuário
@bp.route("/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    dados = request.get_json()
    usuario.nome = dados.get("nome", usuario.nome)
    usuario.cidade = dados.get("cidade", usuario.cidade)
    db.session.commit()
    return jsonify(usuario.to_dict())


# Deletar usuário
@bp.route("/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário excluído com sucesso"})
