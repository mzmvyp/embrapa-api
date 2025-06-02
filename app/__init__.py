from flask import Flask
from flask_restx import Api
from config import Config
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
    }
}

api = Api(app,
          version='1.0',
          title='API de Dados da Embrapa',
          description='API para raspagem e consulta de dados da Embrapa.',
          doc='/swagger-ui',
          security='BearerAuth',
          authorizations=authorizations)

from app.auth import auth_ns
from app.embrapa import embrapa_ns

api.add_namespace(auth_ns)
api.add_namespace(embrapa_ns)

auth_ns.security = [{'BearerAuth': []}]
embrapa_ns.security = [{'BearerAuth': []}]

@app.before_request
def log_headers():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")  # Apenas para debug, remova em produção
