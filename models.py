from extensions import db  # Import db from extensions.py

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    # Define the relationship back to Recipe model using back_populates
    recipes = db.relationship('Recipe', back_populates='category', lazy='dynamic', overlaps="recipes")


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    ingredients = db.Column(db.String(255))
    steps = db.Column(db.String(255))
    url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='recipe')
