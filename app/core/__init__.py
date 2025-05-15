# 9. app/core/__init__.py
# Este arquivo __init__.py torna o diretório 'core' um pacote do Python.
from .exceptions import EmbrapaException
from .security import token_required
from .web_scraper import extrair_dados_generico, extrair_dados_producao, extrair_dados_processamento, extrair_dados_comercializacao, extrair_dados_importacao, extrair_dados_exportacao

__all__ = ['EmbrapaException', 'token_required', 'extrair_dados_generico', 'extrair_dados_producao', 'extrair_dados_processamento', 'extrair_dados_comercializacao', 'extrair_dados_importacao', 'extrair_dados_exportacao']
