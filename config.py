import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'embrapa_secret' # Use uma variável de ambiente em produção