class Config:
    SECRET_KEY = 'embrapa_secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_3w8CmUJnYbMo@ep-square-dream-actspwqu-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_CREATION_SECRET = 'chave_super_secreta'  # chave para autorizar criação de usuário
    SQLALCHEMY_POOL_RECYCLE = 3600