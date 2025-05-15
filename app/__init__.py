from flask import Flask
from flask_restx import Api
import logging
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa a API do Flask-RESTx aqui, passando a instância do Flask
api = Api(app,
    version='1.0',
    title='Embrapa Data API',
    description='A API para acessar dados de viticultura da Embrapa.',
    doc='/swagger/',
)

# Importa o namespace do blueprint
from .api import api_namespace
# Registra o namespace no objeto Api
api.add_namespace(api_namespace)

from .api.resources.auth import auth_ns
api.add_namespace(auth_ns)