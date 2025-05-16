from flask_restx import Resource
from flask import current_app
from app.auth import auth_ns
from app.models import User
from app import db
import datetime
import jwt
from flask_restx.reqparse import RequestParser

register_parser = RequestParser()
register_parser.add_argument('username', type=str, required=True, help='Nome de usuário')
register_parser.add_argument('password', type=str, required=True, help='Senha')
register_parser.add_argument('secret_key', type=str, required=True, help='Chave especial para criação')

login_parser = RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Nome de usuário')
login_parser.add_argument('password', type=str, required=True, help='Senha')

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_parser)
    def post(self):
        args = register_parser.parse_args()
        if args['secret_key'] != current_app.config['USER_CREATION_SECRET']:
            return {'message': 'Chave especial inválida'}, 403

        if User.query.filter_by(username=args['username']).first():
            return {'message': 'Usuário já existe'}, 400

        user = User(username=args['username'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'Usuário criado com sucesso'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            payload = {
                'sub': user.username,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            return {'token': token}, 200
        return {'message': 'Credenciais inválidas'}, 401
