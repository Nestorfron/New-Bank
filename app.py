import os
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from flask_admin import Admin
from dotenv import load_dotenv
from src.api.models import db
from src.api.routes import api
from src.api.admin import setup_admin
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

load_dotenv()


app = Flask(__name__)

CORS(app) 

app.url_map.strict_slashes = False

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', "sqlite:////tmp/test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("FLASK_APP_KEY")

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)

# Configurar Flask-Admin
setup_admin(app)

JWTManager(app)

# Registrar rutas del API
app.register_blueprint(api, url_prefix='/api')

# Ruta principal
@app.route('/')
def home():
    return "Bienvenido a la aplicación Flask", 200

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
