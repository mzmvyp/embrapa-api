from flask_restx import fields

embrapa_data_model = {
    'Produto': fields.String(description='Nome do produto'),
    'Quantidade': fields.Raw(description='Quantidade do produto'),
    'Valor': fields.Raw(description='Valor do produto (US$)'),
}

cultivar_data_model = {
    'Cultivar': fields.String(description='Nome da cultivar'),
    'Quantidade (Kg)': fields.Raw(description='Quantidade em Kg'),
}

token_model = {'token': fields.String(description='JWT token')}