from app import db


class FotoProduto(db.Model):
    __tablename__ = "foto_produto"

    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(255), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
