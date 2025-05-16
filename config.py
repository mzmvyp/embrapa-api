class Config:
    SECRET_KEY = 'embrapa_secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/ambrapa_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_CREATION_SECRET = 'chave_super_secreta'  # chave para autorizar criação de usuário
