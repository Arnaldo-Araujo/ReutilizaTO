from app import db


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"
