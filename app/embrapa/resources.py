from flask_restx import Resource
from flask import jsonify
from app.models import embrapa_data_model
from app.utils import token_required
from app.embrapa import embrapa_ns
from app.embrapa.extractors import (
    extrair_dados_generico,
    extrair_dados_producao,
    extrair_dados_processamento,
    extrair_dados_comercializacao,
    extrair_dados_importacao,
    extrair_dados_exportacao,
)
from flask_restx.reqparse import RequestParser

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

embrapa_parser = RequestParser()
embrapa_parser.add_argument('ano', type=int, default=2020, help='Ano dos dados')
embrapa_parser.add_argument('aba', type=str, required=True, help='Aba para recuperar os dados (Producao, etc.)')
embrapa_parser.add_argument('subopcao', type=str, help='Sub-opção para abas como Importacao/Exportacao')

@embrapa_ns.route('/')
class EmbrapaDataResource(Resource):
    @embrapa_ns.doc('get_embrapa_data', security="Bearer Auth")
    @embrapa_ns.expect(embrapa_parser)
    @embrapa_ns.response(200, 'Success', model=[embrapa_data_model])
    @embrapa_ns.response(400, 'Invalid request')
    @embrapa_ns.response(401, 'Authentication required')
    @embrapa_ns.response(500, 'Internal server error')
    @token_required
    def get(self):
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
                    return jsonify(df.to_dict(orient="records"))
                else:
                    return {
                        'error': f"Não foi possível extrair os dados da aba {nome_aba}."
                    }, 500
            except Exception as e:
                import logging
                logging.error(f"Erro na tentativa {tentativa}: {e}")
                if tentativa < tentativas:
                    import time
                    time.sleep(intervalo_tentativas)
                else:
                    return {'error': str(e)}, 500
