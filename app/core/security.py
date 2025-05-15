from functools import wraps
from flask import request, jsonify
import jwt
from app import app  # Importa a instância do app

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            token = token.split(" ")[1]  # Remove "Bearer "
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401
        except Exception as e:
            return jsonify({'message': f'Erro ao decodificar token: {e}'}), 401

        return f(*args, **kwargs)
    return decorated_function