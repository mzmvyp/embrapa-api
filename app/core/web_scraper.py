# 9. app/core/web_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd
import traceback
import logging

def extrair_dados_generico(nome_aba, url_aba, extrator_aba, tentativas=5, intervalo_tentativas=20):
    """
    Extrai os dados da aba especificada do site usando a funcao extratora fornecida.

    Args:
        nome_aba (str): O nome da aba (para usar nos nomes de arquivos).
        url_aba (str): A URL da aba a ser extraída.
        extrator_aba (callable): Uma funcao que extrai os dados da aba.
        tentativas (int): Número máximo de tentativas de conexão.
        intervalo_tentativas (int): Intervalo em segundos entre as tentativas.

    Returns:
        pandas.DataFrame: Um DataFrame com os dados extraídos.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    df = pd.DataFrame()
    mensagem_erro = None

    for tentativa in range(1, tentativas + 1):
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url_aba)
            logging.info(f"Tentativa {tentativa} de acessar {url_aba}")
            driver.implicitly_wait(3)
            df = extrator_aba(driver)
            logging.info("Dados extraídos com sucesso!")
            break  # Se a extração for bem-sucedida, saia do loop

        except WebDriverException as e:
            mensagem_erro = f"Erro de WebDriver na tentativa {tentativa}: {e}"
            logging.error(mensagem_erro)
            traceback.print_exc()
            if "net::ERR_CONNECTION_REFUSED" in str(e):
                if tentativa < tentativas:
                    logging.info(f"Tentando novamente em {intervalo_tentativas} segundos...")
                    time.sleep(intervalo_tentativas)
                else:
                    mensagem_erro = "Número máximo de tentativas excedido. Falha ao extrair os dados."
                    logging.error(mensagem_erro)
                    break
            else:
                raise  # Relança outros erros de WebDriver
        except Exception as e:
            mensagem_erro = f"Erro inesperado na tentativa {tentativa}: {e}"
            logging.error(mensagem_erro)
            traceback.print_exc()
            if tentativa < tentativas:
                logging.info(f"Tentando novamente em {intervalo_tentativas} segundos...")
                time.sleep(intervalo_tentativas)
            else:
                mensagem_erro = "Número máximo de tentativas excedido. Falha ao extrair os dados."
                logging.error(mensagem_erro)
                break
        finally:
            driver.quit()

    if mensagem_erro:
        raise Exception(mensagem_erro)
    return df


def extrair_dados_producao(driver):
    """Extrai os dados da aba de Producao."""
    try:
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.tb_base.tb_dados"))
        )
        cabecalho = ["Produto", "Quantidade (ton)"]
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:
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
                )
            )
        )
        cabecalho = ["Produto", "Valor"]
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:
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
                )
            )
        )
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:
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
                )
            )
        )
        cabecalho = ["Produto", "Quantidade", "Valor (US$)"]
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        for linha in linhas[1:]:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(cabecalho):
                dado = {}
                for i, coluna in enumerate(cabecalho):
                    dado[coluna] = celulas[i].text.strip()
                dados.append(dado)
        return pd.DataFrame(dados)
    except Exception as e:
        raise Exception(f"Erro ao extrair dados de Exportacao: {e}")

