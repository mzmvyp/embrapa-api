from flask_restx import Namespace

auth_ns = Namespace('auth', description='Autenticação')

from .resources import *
