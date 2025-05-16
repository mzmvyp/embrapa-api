from flask_restx import Namespace

embrapa_ns = Namespace('embrapa', description='Operações relacionadas aos dados da Embrapa')

from .resources import *
