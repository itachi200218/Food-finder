# models.py
from extensions import db  # Import db from extensions.py

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    ingredients = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    steps = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Recipe {self.name}>"