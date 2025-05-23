from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
import enum


class TipoUsuarioEnum(enum.Enum):
    administrador = "administrador"
    beneficiario = "beneficiario"
    ong = "ong"
    doador = "doador"


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(
        db.Enum(TipoUsuarioEnum), nullable=False, default=TipoUsuarioEnum.doador
    )
    cidade = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "cidade": self.cidade,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
