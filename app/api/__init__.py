from flask import Blueprint
from flask_restx import Api, Namespace  # Importa Api e Namespace

# Cria o blueprint
api_blueprint = Blueprint('embrapa_api', __name__, url_prefix='/embrapa')

# Inicializa o Api
api = Api(api_blueprint)

# Cria o namespace
api_namespace = Namespace('embrapa', description='Operações relacionadas aos dados da Embrapa')

# Adiciona o namespace ao Api
api.add_namespace(api_namespace)

from .resources.embrapa_data import EmbrapaDataResource