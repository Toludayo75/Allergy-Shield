from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    allergens = db.relationship('UserAllergen', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    # description = db.Column(db.Text)
    users = db.relationship('UserAllergen', backref='allergen', lazy=True)

class UserAllergen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    allergen_id = db.Column(db.Integer, db.ForeignKey('allergen.id'), nullable=False)
    severity = db.Column(db.String(20))  # mild, moderate, severe

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    nafdac_number = db.Column(db.String(20), unique=True)
    ingredients = db.relationship('ProductIngredient', backref='product', lazy=True)

class ProductIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    ingredient_name = db.Column(db.String(64), nullable=False)
    is_allergen = db.Column(db.Boolean, default=False)
