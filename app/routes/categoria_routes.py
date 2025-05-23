from flask import Blueprint, request, jsonify
from app import db
from app.models.categoria import Categoria

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


# Listar todas
@bp.route("/", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([{"id": c.id, "nome": c.nome} for c in categorias])


# Cadastrar nova
@bp.route("/", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json()
    categoria = Categoria(nome=dados["nome"])
    db.session.add(categoria)
    db.session.commit()
    return jsonify({"id": categoria.id, "nome": categoria.nome}), 201


# Atualizar
@bp.route("/<int:id>", methods=["PUT"])
def atualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    dados = request.get_json()
    categoria.nome = dados["nome"]
    db.session.commit()
    return jsonify({"id": categoria.id, "nome": categoria.nome})


# Remover
@bp.route("/<int:id>", methods=["DELETE"])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"mensagem": "Categoria removida com sucesso."})
