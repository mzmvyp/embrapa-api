import logging
import traceback
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Removido Selenium imports (já feito anteriormente)

def extrair_dados_generico(nome_aba, url, extrator_aba):
    try:
        # Faz a requisição HTTP para a URL
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para status de erro HTTP (4xx ou 5xx)

        # --- INÍCIO DA MODIFICAÇÃO PARA TRATAMENTO DE ENCODING ---
        # 1. Tenta detectar o encoding automaticamente
        response.encoding = response.apparent_encoding

        # Opcional: Se a detecção automática falhar e você souber o encoding (ex: 'iso-8859-1' ou 'utf-8')
        # você pode forçar. Use isso APENAS se a detecção automática não funcionar.
        # response.encoding = 'iso-8859-1' # Ou 'utf-8'

        # Cria um objeto BeautifulSoup para parsear o HTML
        # Passamos response.text, que agora deve ter o encoding correto
        soup = BeautifulSoup(response.text, 'lxml')
        # --- FIM DA MODIFICAÇÃO PARA TRATAMENTO DE ENCODING ---

        # Agora, passamos o objeto 'soup' para a função extratora
        df = extrator_aba(soup)
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de requisição HTTP ao extrair dados da aba {nome_aba} de {url}: {e}")
        logging.error(traceback.format_exc())
        raise e
    except Exception as e:
        logging.error(f"Erro ao extrair dados genéricos da aba {nome_aba}: {e}")
        logging.error(traceback.format_exc())
        raise e

# --- As funções de extração (extrair_dados_producao, extrair_dados_processamento, etc.)
# permanecem as mesmas, pois a modificação do encoding é feita antes de BeautifulSoup. ---

def extrair_dados_producao(soup):
    """Extrai os dados da aba de Producao usando BeautifulSoup."""
    try:
        tabela = soup.select_one("table.tb_base.tb_dados")
        if not tabela:
            raise Exception("Tabela de Producao não encontrada no HTML.")
        cabecalho = ["Produto", "Quantidade (ton)"]
        dados = []
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:
            celulas = linha.find_all("td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].get_text(strip=True)
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Producao: {e}")

def extrair_dados_processamento(soup):
    """Extrai os dados da aba de Processamento usando BeautifulSoup."""
    try:
        tabela = soup.select_one("table.tb_base.tb_dados")
        if not tabela:
            raise Exception("Tabela de Processamento não encontrada no HTML.")
        cabecalho = ["Cultivar", "Quantidade (Kg)"]
        dados = []
        linhas = tabela.find_all("tr")
        for linha in linhas[1:-1]:
            celulas = linha.find_all("td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].get_text(strip=True)
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Processamento: {e}")

def extrair_dados_comercializacao(soup):
    """Extrai os dados da aba de Comercializacao usando BeautifulSoup."""
    try:
        tabela = soup.select_one("table.tb_base.tb_dados")
        if not tabela:
            raise Exception("Tabela de Comercializacao não encontrada no HTML.")
        cabecalho = ["Produto", "Valor"]
        dados = []
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:
            celulas = linha.find_all("td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].get_text(strip=True)
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Comercializacao: {e}")

def extrair_dados_importacao(soup):
    """Extrai os dados da aba de Importacao usando BeautifulSoup."""
    try:
        tabela = soup.select_one("table.tb_base.tb_dados")
        if not tabela:
            raise Exception("Tabela de Importacao não encontrada no HTML.")
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]
        dados = []
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:
            celulas = linha.find_all("td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].get_text(strip=True)
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Importacao: {e}")

def extrair_dados_exportacao(soup):
    """Extrai os dados da aba de Exportacao usando BeautifulSoup."""
    try:
        tabela = soup.select_one("table.tb_base.tb_dados")
        if not tabela:
            raise Exception("Tabela de Exportacao não encontrada no HTML.")
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]
        dados = []
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:
            celulas = linha.find_all("td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].get_text(strip=True)
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Exportacao: {e}")