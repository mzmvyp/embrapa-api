from flask_restx import reqparse

embrapa_parser = reqparse.RequestParser()
embrapa_parser.add_argument('ano', type=int, default=2020, help='Ano dos dados')
embrapa_parser.add_argument('aba', type=str, required=True, help='Aba para recuperar os dados (Producao, etc.)')
embrapa_parser.add_argument('subopcao', type=str, help='Sub-opção para abas como Importacao/Exportacao')

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True, help='Nome de usuário')
auth_parser.add_argument('password', type=str, required=True, help='Senha')