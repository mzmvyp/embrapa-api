import time
from flask_restx import Namespace, Resource, marshal
from flask import jsonify
from ..parsers import embrapa_parser
from ..models import embrapa_data_model, cultivar_data_model
from selenium.common.exceptions import WebDriverException
from ...core.web_scraper import extrair_dados_generico, extrair_dados_producao, extrair_dados_processamento, extrair_dados_comercializacao, extrair_dados_importacao, extrair_dados_exportacao
from ...core.security import token_required

api = Namespace('embrapa', description='Operações relacionadas aos dados da Embrapa')

ABA_OPCAO_MAP = {
    "Producao": "opt_02",
    "Processamento": "opt_03",
    "Comercializacao": "opt_04",
    "Importacao": "opt_05",
    "Exportacao": "opt_06",
}

SUBMENU_PROCESSAMENTO_MAP = {
    "Viniferas": "subopt_01",
    "Americanas_e_hibridas": "subopt_02",
    "Uvas_de_mesa": "subopt_03",
    "Sem_classificacao": "subopt_04",
}

SUBMENU_IMPORTACAO_MAP = {
    "Vinhos_de_mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas_frescas": "subopt_03",
    "Uvas_passas": "subopt_04",
    "Suco_de_uva": "subopt_05",
}

SUBMENU_EXPORTACAO_MAP = {
    "Vinhos_de_mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas_frescas": "subopt_03",
    "Suco_de_uva": "subopt_04",
}

@api.route('/')
class EmbrapaDataResource(Resource):
    @api.doc('get_embrapa_data', security="Bearer Auth")
    @api.expect(embrapa_parser)
    @api.response(200, 'Success', model=[embrapa_data_model])
    @api.response(400, 'Invalid request')
    @api.response(401, 'Authentication required')
    @api.response(500, 'Internal server error')
    @token_required
    def get(self):
        """
        Recupera dados do site da Embrapa.
        """
        args = embrapa_parser.parse_args()
        ano = args['ano']
        nome_aba = args['aba']
        nome_submenu_api = args['subopcao']

        if not nome_aba:
            return {'error': "Parâmetro 'aba' é obrigatório."}, 400

        try:
            opcao = ABA_OPCAO_MAP[nome_aba]
        except KeyError:
            return {'error': f"Aba '{nome_aba}' não encontrada."}, 400

        url_base = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}"

        extrator_aba = None
        if nome_aba in ["Processamento", "Importacao", "Exportacao"]:
            submenu_map = None
            if nome_aba == "Processamento":
                submenu_map = SUBMENU_PROCESSAMENTO_MAP
                extrator_aba = extrair_dados_processamento
            elif nome_aba == "Importacao":
                submenu_map = SUBMENU_IMPORTACAO_MAP
                extrator_aba = extrair_dados_importacao
            elif nome_aba == "Exportacao":
                submenu_map = SUBMENU_EXPORTACAO_MAP
                extrator_aba = extrair_dados_exportacao

            try:
                subopcao = submenu_map[nome_submenu_api]
                url = f"{url_base}&subopcao={subopcao}"
            except KeyError:
                return {
                    'error': f"Submenu '{nome_submenu_api}' não encontrado para a aba {nome_aba}."
                }, 400
        else:
            url = url_base
            if nome_aba == "Producao":
                extrator_aba = extrair_dados_producao
            elif nome_aba == "Comercializacao":
                extrator_aba = extrair_dados_comercializacao
            else:
                return {'error': f"Aba '{nome_aba}' não suportada."}, 400

        tentativas = 3
        intervalo_tentativas = 5

        for tentativa in range(1, tentativas + 1):
            try:
                df = extrair_dados_generico(nome_aba, url, extrator_aba)
                if not df.empty:
                    if nome_aba == "Processamento":
                        return jsonify([marshal(record, cultivar_data_model) for record in df.to_dict(orient="records")])
                    else:
                        return jsonify([marshal(record, embrapa_data_model) for record in df.to_dict(orient="records")])
                else:
                    return {
                        'error': f"Não foi possível extrair os dados da aba {nome_aba}."
                    }, 500
            except Exception as e:
                api.logger.error(f"Erro na tentativa {tentativa}: {e}")
                if tentativa < tentativas:
                    api.logger.info(f"Tentando novamente em {intervalo_tentativas} segundos...")
                    time.sleep(intervalo_tentativas)
                else:
                    return {'error': f"Falha ao extrair dados após {tentativas} tentativas: {e}"}, 500
                
            except WebDriverException as e:
                api.logger.error(f"Erro de WebDriver na tentativa {tentativa}: {e}")
                if tentativa < tentativas:
                    api.logger.info(f"Tentando novamente em {intervalo_tentativas} segundos...")
                    time.sleep(intervalo_tentativas)
                else:
                    return {'error': f"Falha ao inicializar o WebDriver após {tentativas} tentativas: {e}"}, 500

        return {'error': f"Falha ao obter os dados após {tentativas} tentativas."}, 500