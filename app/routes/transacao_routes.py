from flask import Blueprint, request, jsonify
from app import db
from app.models.transacao import Transacao

bp = Blueprint("transacoes", __name__, url_prefix="/transacoes")


# Listar todas ou por usuário
@bp.route("/", methods=["GET"])
def listar_transacoes():
    usuario_id = request.args.get("usuario")
    if usuario_id:
        transacoes = Transacao.query.filter(
            (Transacao.de_usuario_id == usuario_id)
            | (Transacao.para_usuario_id == usuario_id)
        ).all()
    else:
        transacoes = Transacao.query.all()

    return jsonify([t.to_dict() for t in transacoes])


# Registrar nova transação
@bp.route("/", methods=["POST"])
def criar_transacao():
    dados = request.get_json()

    transacao = Transacao(
        tipo=dados["tipo"],
        produto_id=dados["produto_id"],
        de_usuario_id=dados["de_usuario_id"],
        para_usuario_id=dados["para_usuario_id"],
    )

    db.session.add(transacao)
    db.session.commit()

    return jsonify(transacao.to_dict()), 201


# Deletar transação (cancelamento)
@bp.route("/<int:id>", methods=["DELETE"])
def excluir_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    return jsonify({"mensagem": "Transação excluída com sucesso"})
