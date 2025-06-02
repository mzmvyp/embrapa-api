from flask import request, jsonify, current_app
from functools import wraps
import jwt

from functools import wraps
from flask import request, g
import jwt
from app import app
from app.models import User
from datetime import datetime, timedelta

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Espera "Bearer <token>"
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                # Caso o header Authorization esteja presente mas não no formato esperado
                return {'message': 'Formato de token inválido. Use "Bearer <token>"'}, 401


        if not token:
            # CORREÇÃO AQUI: Retorne um dicionário e um código de status
            return {'message': 'Token de autenticação está faltando!'}, 401

        try:
            # Decodifica o token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # Verifica se o 'user_id' está presente no payload do token
            user_id = data.get('user_id')
            if not user_id:
                # CORREÇÃO AQUI: Retorne um dicionário e um código de status
                return {'message': 'Token inválido: ID de usuário ausente no token!'}, 401

            current_user = User.query.get(user_id)
            if not current_user:
                # CORREÇÃO AQUI: Retorne um dicionário e um código de status
                return {'message': 'Token inválido: Usuário não encontrado!'}, 401
            g.current_user = current_user # Armazena o usuário logado para uso no endpoint
        except jwt.ExpiredSignatureError:
            # CORREÇÃO AQUI: Retorne um dicionário e um código de status
            return {'message': 'Token de autenticação expirado!'}, 401
        except jwt.InvalidTokenError:
            # CORREÇÃO AQUI: Retorne um dicionário e um código de status
            return {'message': 'Token de autenticação inválido!'}, 401
        except Exception as e:
            # CORREÇÃO AQUI: Retorne um dicionário e um código de status
            return {'message': f'Erro ao processar token: {str(e)}'}, 401

        return f(*args, **kwargs)
    return decorated

def generate_token(user_id):
    payload = {
        'user_id': user_id, # Assumindo que o ID do usuário é o que você quer no token
        'exp': datetime.utcnow() + timedelta(minutes=60) # Token expira em 60 minutos
    }
    # No seu resources.py de login, o payload usa 'sub': user.username
    # Certifique-se de que generate_token seja usado para gerar os tokens de autenticação
    # ou ajuste o payload aqui para refletir 'sub' se preferir.
    # Se você está usando o ID, este é o correto.
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')