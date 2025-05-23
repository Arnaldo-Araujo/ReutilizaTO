from flask import Blueprint, request, jsonify
from app import db
from app.models.produto import Produto

bp = Blueprint("produtos", __name__, url_prefix="/produtos")


# Listar todos os produtos
@bp.route("/", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])


# Cadastrar produto
@bp.route("/", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    produto = Produto(
        nome=dados["nome"],
        descricao=dados.get("descricao", ""),
        condicao=dados.get("condicao", "usado"),
        status=dados.get("status", "disponivel"),
        usuario_id=dados["usuario_id"],
        categoria_id=dados["categoria_id"],
        foto=dados.get("foto", None),
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201


# Atualizar produto
@bp.route("/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    dados = request.get_json()
    produto.nome = dados.get("nome", produto.nome)
    produto.descricao = dados.get("descricao", produto.descricao)
    produto.condicao = dados.get("condicao", produto.condicao)
    produto.status = dados.get("status", produto.status)
    produto.foto = dados.get("foto", produto.foto)
    db.session.commit()
    return jsonify(produto.to_dict())


# Deletar produto
@bp.route("/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto excluído com sucesso"})
