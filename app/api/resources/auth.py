from flask_restx import Namespace, Resource
from flask import jsonify
import jwt
import datetime
from ..parsers import auth_parser
from ..models import token_model
from flask import current_app # Importa current_app
from app.core.security import token_required  # Importa o decorator

auth_ns = Namespace('auth', description='Autenticação')

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(auth_parser)
    @auth_ns.marshal_with(token_model)
    def post(self):
        """
        Gera um token JWT para autenticação.
        """
        args = auth_parser.parse_args()
        username = args['username']
        password = args['password']

        # Aqui você precisa verificar as credenciais do usuário
        # Em um sistema real, você consultaria um banco de dados
        # ou um serviço de autenticação.
        if username == 'admin' and password == 'password':
            # Gere o token JWT
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            payload = {
                'sub': username,
                'exp': expiration_time,
                'iat': datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256') # Usa current_app
            return {'token': token}, 200
        else:
            return {'message': 'Credenciais inválidas'}, 401