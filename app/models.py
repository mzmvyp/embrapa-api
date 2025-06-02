from flask_restx import fields
from app import api
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import scrypt

# Mantenha os outros modelos e definições abaixo da classe DadosRaspar
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # armazena o hash da senha
    
    def set_password(self, senha_pura):
        self.password = scrypt.hash(senha_pura)  # hash com scrypt

    def check_password(self, senha_pura):
        print(f"Senha recebida para verificação: {senha_pura}")
        print(f"Hash armazenado no banco: {self.password}")
        resultado = scrypt.verify(senha_pura, self.password) # compara com scrypt
        print(f"Resultado da verificação: {resultado}")
        return resultado

embrapa_data_model = api.model(
    'EmbrapaData',
    {
        'Produto': fields.String(description='Nome do produto'),
        'Quantidade': fields.Raw(description='Quantidade do produto'),
        'Valor': fields.Raw(description='Valor do produto (US$)'),
    },
)

cultivar_data_model = api.model(
    'CultivarData',
    {
        'Cultivar': fields.String(description='Nome da cultivar'),
        'Quantidade (Kg)': fields.Raw(description='Quantidade em Kg')
    },
)

token_model = api.model('Token', {'token': fields.String(description='JWT token')})