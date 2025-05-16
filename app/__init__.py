from flask import Flask
from flask_restx import Api
from config import Config
import logging
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

api = Api(
    app,
    version='1.0',
    title='Embrapa Data API',
    description='API para acessar dados de viticultura da Embrapa.',
    doc='/swagger/',
)

from app.auth import auth_ns
from app.embrapa import embrapa_ns

api.add_namespace(auth_ns)
api.add_namespace(embrapa_ns)




