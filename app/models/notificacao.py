from app import db
from datetime import datetime


class Notificacao(db.Model):
    __tablename__ = "notificacao"

    id = db.Column(db.Integer, primary_key=True)

    transmissor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )  # receptor

    interesse_id = db.Column(db.Integer, db.ForeignKey("transacao.id"), nullable=True)

    mensagem = db.Column(db.Text, nullable=False)
    lido = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "transmissor_id": self.transmissor_id,
            "usuario_id": self.usuario_id,
            "interesse_id": self.interesse_id,
            "mensagem": self.mensagem,
            "lido": self.lido,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
