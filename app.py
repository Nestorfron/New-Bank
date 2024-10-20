import os
from flask import Flask, send_from_directory, jsonify
from flask_migrate import Migrate, init, migrate, upgrade
from flask_admin import Admin
from dotenv import load_dotenv
from src.api.utils import APIException, generate_sitemap
from src.api.models import db
from src.api.routes import api
from src.api.admin import setup_admin
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

load_dotenv()

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Ruta principal
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
