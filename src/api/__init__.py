from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
# Import all models to ensure they are registered with SQLAlchemy
from .models import *