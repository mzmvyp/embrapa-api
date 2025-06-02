embrapa-api
API de Dados da Embrapa
Este projeto implementa uma API RESTful para acessar e disponibilizar dados raspados da Embrapa, oferecendo autenticação JWT e um mecanismo de fallback para garantir a disponibilidade dos dados.

Visão Geral da Arquitetura
A arquitetura da solução é composta por uma API Flask que serve como interface para o consumo dos dados. Ela prioriza a busca em um banco de dados PostgreSQL para dados atualizados e possui um mecanismo de fallback para arquivos locais (JSON/CSV), garantindo a continuidade do serviço mesmo em caso de problemas com o banco de dados. Um processo de raspagem de dados separado é responsável por popular essas fontes de dados.

Snippet de código

graph TD
    A[Usuário/Cliente] --> B{Requisição de Dados};
    B --> C[API Flask];
    C --> D{Tentar buscar no Banco de Dados (PostgreSQL)};
    D -- Sucesso --> E[Dados do Banco de Dados];
    D -- Falha --> F{Fallback: Tentar ler de Arquivo Local (JSON/CSV)};
    F -- Sucesso --> G[Dados do Arquivo Local];
    E --> H[API Formata e Retorna Dados];
    G --> H;
    H --> I[Resposta para Usuário/Cliente];

    subgraph Fontes de Dados
        D
        F
    end
    subgraph Raspagem (Processo Opcional, Fora da API)
        J[Script de Raspagem/Coleta] --> K[Salvar no Banco de Dados];
        J --> L[Salvar em Arquivo Local];
    end

    K --> D;
    L --> F;
Fluxo Detalhado:

Usuário/Cliente: Inicia uma requisição de dados para a API.
API Flask: Recebe a requisição e processa a lógica de autenticação e busca de dados.
Busca no Banco de Dados: A API tenta primeiramente obter os dados do banco de dados PostgreSQL, que deve conter os dados mais atualizados provenientes da raspagem.
Fallback para Arquivo Local: Em caso de falha na comunicação ou acesso ao banco de dados, a API tenta ler os dados de um arquivo local previamente gerado pelo processo de raspagem.
Formatação e Retorno: Independentemente da fonte, a API formata os dados para o padrão JSON e os envia de volta ao usuário/cliente.
Funcionalidades
Autenticação JWT (JSON Web Token): Protege as rotas da API, garantindo que apenas usuários autorizados possam acessá-las.
API RESTful: Disponibiliza os dados de forma programática através de rotas claras e padronizadas.
Mecanismo de Fallback: Garante a disponibilidade dos dados através de uma fonte local, caso o banco de dados principal esteja inacessível.
Documentação Interativa: Swagger UI para explorar e testar os endpoints da API.
Tecnologias Utilizadas
Python 3.x
Flask: Framework web para construir a API.
Flask-RESTx: Extensão para Flask que facilita a criação de APIs REST e a geração de documentação Swagger.
Flask-SQLAlchemy: ORM para interação com o banco de dados.
Psycopg2: Adaptador PostgreSQL para Python.
PyJWT: Para geração e validação de JWT.
SQLAlchemy-Utils: Utilitários para SQLAlchemy.
Werkzeug: Biblioteca de utilitários para Python WSGI.
PostgreSQL: Banco de dados relacional para armazenamento primário dos dados.
Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:

Python 3.x
pip (gerenciador de pacotes do Python)
PostgreSQL (servidor de banco de dados rodando e acessível)
Configuração do Ambiente
Siga os passos abaixo para configurar e rodar o projeto localmente:

Clonar o Repositório:

Bash

git clone **<URL_DO_SEU_REPOSITORIO>**
cd embrapa-api
Criar e Ativar Ambiente Virtual:
É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
Instalar Dependências:
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias.

Bash

pip install -r requirements.txt
Configurar o Banco de Dados:
A API se conecta a um banco de dados PostgreSQL. Crie um banco de dados e um usuário para a aplicação.

Variáveis de Ambiente: Configure suas credenciais do banco de dados e outras configurações sensíveis em um arquivo chamado .env na raiz do projeto, ou diretamente no seu arquivo config.py.
Exemplo de conteúdo para o arquivo .env:

DATABASE_URL=postgresql://**<seu_usuario_db>**:**<sua_senha_db>**@localhost:5432/**<seu_nome_db>**
JWT_SECRET_KEY=**<uma_chave_secreta_forte_para_JWT_gere_uma_aleatoria>**
Certifique-se de que seu código está lendo essas variáveis de ambiente. Se você configurou diretamente em config.py, insira as credenciais lá.

Criação de Tabelas e Usuário Inicial: A API deve criar as tabelas necessárias e um usuário padrão na primeira execução ou via um script de inicialização.
Para criar um usuário inicial (se não for feito automaticamente pela sua API), você pode executar um script Python separado (ex: create_user.py):

Python

# Exemplo de create_user.py ou parte da sua inicialização:
# from app.models import db, User
# from app import create_app
#
# app = create_app()
# with app.app_context():
#     db.create_all() # Garante que as tabelas existem
#     if not User.query.filter_by(username='**<nome_de_usuario_inicial>**').first():
#         user = User(username='**<nome_de_usuario_inicial>**', password='**<senha_inicial>**') # A senha deve ser hashed
#         db.session.add(user)
#         db.session.commit()
#         print("Usuário inicial criado com sucesso!")
Certifique-se de que as senhas sejam armazenadas como hashes no banco de dados e que o script de criação de usuário/tabelas seja executado pelo menos uma vez.

Como Rodar a API
Com o ambiente virtual ativado e as configurações do banco de dados prontas:

Bash

python run.py
A API estará disponível em http://127.0.0.1:5000/.

Uso da API
Acessando a Documentação Interativa (Swagger UI)
A documentação completa e interativa da API está disponível no Swagger UI, onde você pode explorar e testar todos os endpoints:

Acesse: http://127.0.0.1:5000/swagger-ui

Autenticação
Todas as rotas de dados requerem autenticação via JWT (JSON Web Token).

Obter um Token de Autenticação:
Envie uma requisição POST para o endpoint de login com seu nome de usuário e senha.

Rota: /auth/login
Método: POST
Parâmetros (Query Params): username, password
Exemplo via PowerShell:

PowerShell

$BaseURL = "http://127.0.0.1:5000"
$Username = "**<seu_usuario_inicial>**"
$Password = "**<sua_senha_inicial>**"

$LoginURL = "$BaseURL/auth/login?username=$Username&password=$Password"
$LoginResponse = Invoke-RestMethod -Uri $LoginURL -Method Post
$Token = $LoginResponse.token
Write-Host "Token JWT obtido: $Token"
Você receberá um JSON contendo o seu token JWT. Copie este token.

Usar o Token para Acessar Rotas Protegidas:
Para acessar as rotas protegidas (como /embrapa/), inclua o token no cabeçalho Authorization com o prefixo Bearer (espaço após "Bearer").

Exemplo via PowerShell (com o token obtido):

PowerShell

$AnoTeste = 2002 # Altere o ano conforme necessário
$Aba = "Producao" # Altere a aba conforme necessário

$DataURL = "$BaseURL/embrapa/?ano=$AnoTeste&aba=$Aba"
$Headers = @{ "Authorization" = "Bearer $Token" }

$DataResponse = Invoke-RestMethod -Uri $DataURL -Method Get -Headers $Headers
Write-Host "Dados da Embrapa para $AnoTeste ($Aba):"
$DataResponse | ConvertTo-Json -Depth 10 # Para exibir o JSON completo
Rotas Principais
POST /auth/login

Descrição: Autentica um usuário e retorna um token JWT.
Parâmetros: username (string), password (string).
Exemplo de Resposta: {"token": "eyJ..."}
GET /embrapa/

Descrição: Retorna dados da Embrapa com base nos filtros de ano e tipo de aba.
Parâmetros: ano (int, obrigatório), aba (string, obrigatório - ex: "Producao", "Comercializacao", "Importacao", "Exportacao", "Processamento").
Autenticação: Requer token JWT válido no cabeçalho Authorization.
Exemplo de Resposta:
JSON

[
  {
    "Produto": "VINHO DE MESA",
    "Quantidade (ton)": "259.589.740"
  },
  {
    "Produto": "Tinto",
    "Quantidade (ton)": "215.892.333"
  }
  // ... mais dados
]
Processo de Raspagem de Dados (População do Banco/Arquivo)
Este projeto assume que o banco de dados (e/ou o arquivo local para fallback) é populado por um script de raspagem de dados externo à API.

Para popular o banco de dados/arquivo local: Execute o seu script de raspagem de dados. Exemplo:
Bash

python **<caminho/para/seu_script_de_raspagem>.py**
# Ex: python scripts/scrape_embrapa_data.py
Certifique-se de que este script salve os dados nas fontes configuradas (PostgreSQL e/ou arquivo local).
Resolução de Problemas Comuns
"Token de autenticação está faltando!" (Erro 401 na API):

Causa: O token JWT não foi enviado, ou não foi enviado no formato correto (Authorization: Bearer <token>).
Solução: Verifique se você obteve um token válido e se está incluindo-o no cabeçalho Authorization com o prefixo "Bearer ". Se estiver usando o Swagger UI e este erro persistir (mesmo após autorizar), pode ser um problema de cache/extensões/segurança do navegador. Use ferramentas como Postman, curl ou PowerShell para confirmar que sua API está funcionando corretamente.
psycopg2.OperationalError: SSL SYSCALL error: EOF detected (Erro 500 na API ao acessar o banco):

Causa: Problema de conexão com o banco de dados, geralmente devido a um timeout de inatividade do PostgreSQL que fecha a conexão antes que a aplicação a reutilize.
Solução: Esta issue foi resolvida adicionando SQLALCHEMY_POOL_RECYCLE = 3600 ao seu config.py. Certifique-se de que essa linha está presente e o servidor Flask foi reiniciado após a alteração.
Erros no console do navegador (Access to storage is not allowed from this context.):

Causa: Estes erros são específicos do navegador e indicam que o JavaScript do Swagger UI está sendo impedido de acessar o armazenamento do navegador (mesmo que o localStorage funcione em testes simples). Isso impede o Swagger UI de injetar o token corretamente.
Solução: Sua API funciona corretamente via ferramentas externas. Para o Swagger UI, tente limpar o cache e os dados do site no navegador, desabilitar extensões, tentar o modo anônimo ou um navegador diferente. Para testar a API, use Postman/curl/PowerShell.
Autor
&lt;Willian do Prado Vieira
&lt;https://br.linkedin.com/in/willian-do-prado-vieira-87348659