from app import db
from datetime import datetime


class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # doacao ou troca
    data = db.Column(db.DateTime, default=datetime.utcnow)

    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    de_usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    para_usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    produto = db.relationship("Produto", backref="transacoes")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "data": self.data.strftime("%Y-%m-%d %H:%M:%S"),
            "produto_id": self.produto_id,
            "de_usuario_id": self.de_usuario_id,
            "para_usuario_id": self.para_usuario_id,
        }
