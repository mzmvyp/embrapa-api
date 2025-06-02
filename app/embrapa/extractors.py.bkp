import logging
import traceback
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_dados_generico(nome_aba, url, extrator_aba):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        df = extrator_aba(driver)
        driver.quit()
        return df
    except Exception as e:
        logging.error(f"Erro ao extrair dados genéricos da aba {nome_aba}: {e}")
        logging.error(traceback.format_exc())
        driver.quit()
        raise e

def extrair_dados_producao(driver):
    """Extrai os dados da aba de Producao."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.tb_base.tb_dados"))
        )
        cabecalho = ["Produto", "Quantidade (ton)"]  # Ajuste este cabeçalho!
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:  # Inclui o cabeçalho, ajuste se necessário
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Producao: {e}")



def extrair_dados_processamento(driver):
    """Extrai os dados da aba de Processamento."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.tb_base.tb_dados"))
        )
        cabecalho = ["Cultivar", "Quantidade (Kg)"]
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        for linha in linhas[1:-1]:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)

        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Processamento: {e}")



def extrair_dados_comercializacao(driver):
    """Extrai os dados da aba de Comercializacao."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "table.tb_base.tb_dados",
                )  # Ajuste este seletor!!!
            )
        )
        cabecalho = ["Produto", "Valor"]  # Ajuste este cabeçalho!!!
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:  # Inclui o cabeçalho, ajuste se necessário
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Comercializacao: {e}")



def extrair_dados_importacao(driver):
    """Extrai os dados da aba de Importacao."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "table.tb_base.tb_dados",
                )  # Ajuste este seletor!!!
            )
        )
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]  # Ajuste este cabeçalho!!!
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:  # Inclui o cabeçalho, ajuste se necessário
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Importacao: {e}")



def extrair_dados_exportacao(driver):
    """Extrai os dados da aba de Exportacao."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "table.tb_base.tb_dados",
                )  # Ajuste este seletor!!!
            )
        )
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]  # Ajuste este cabeçalho!!!
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:  # Inclui o cabeçalho, ajuste se necessário
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Exportacao: {e}")