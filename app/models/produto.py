from sqlalchemy import Boolean
from app import db
from datetime import datetime
from app.models.foto_produto import FotoProduto


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    condicao = db.Column(db.String(50))  # novo, usado
    status = db.Column(db.String(20), default="disponivel")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    aprovado = db.Column(Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    fotos = db.relationship("FotoProduto", backref="produto")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "condicao": self.condicao,
            "status": self.status,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "foto": self.foto,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
