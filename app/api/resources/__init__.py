# 6. app/api/resources/__init__.py
# Este arquivo __init__.py torna o diretório 'resources' um pacote do Python.
from .auth import auth_ns
from .embrapa_data import EmbrapaDataResource

__all__ = ['auth_ns', 'EmbrapaDataResource']