import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "mysql+mysqldb://ayo:%23Ayomide2005@localhost/allergy_detection")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable event system for better performance

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# initialize the app with the extension
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import routes after app initialization to avoid circular imports
with app.app_context():
    import routes
    import models

def init_db():
    #import models here to avoid circular imports
    from models import User, Allergen
    db.create_all()

 # Pre-populate allergens if the table is empty
    if not Allergen.query.first():
        common_allergens = [
            "Peanuts",
            "Milk",
            "Eggs",
            "Fish",
            "Soy",
            "Wheat",
            "Tree Nuts",
            "Shellfish"
        ]
        for name in common_allergens:
            allergen = Allergen(name=name)
            db.session.add(allergen)
        db.session.commit()

# Import routes
from routes import *