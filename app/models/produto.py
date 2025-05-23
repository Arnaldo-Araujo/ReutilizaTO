from app import db
from datetime import datetime


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    foto = db.Column(db.String(255))  # pode armazenar caminho da imagem
    condicao = db.Column(db.String(50))  # novo, usado
    status = db.Column(db.String(20), default="disponivel")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

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
