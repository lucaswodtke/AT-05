from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
import requests
import os # Importar a biblioteca os para acessar variáveis de ambiente

type_defs = """
    enum Categoria {
        FAMILIAR
        PESSOAL
        COMERCIAL
    }

    enum TipoTelefone {
        MOVEL
        FIXO
        COMERCIAL
    }

    type Telefone {
        numero: String!
        tipo: TipoTelefone!
    }

    input TelefoneInput {
        numero: String!
        tipo: TipoTelefone!
    }

    type Contato {
        id: ID!
        nome: String!
        categoria: Categoria!
        telefones: [Telefone!]
    }

    type Query {
        contatos: [Contato!]
    }

    type Mutation {
        adicionarContato(nome: String!, categoria: Categoria!, telefones: [TelefoneInput!]): Contato
    }
"""

query = QueryType()
mutation = MutationType()


CONTATOS_API_URL = os.getenv("CONTATOS_API_URL", "http://localhost:5001/contatos")


@query.field("contatos")
def resolve_contatos(*_):
    """Resolve a query que busca todos os contatos."""
    try:
        response = requests.get(CONTATOS_API_URL)
        response.raise_for_status() # Lança um erro para status codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar contatos no microsserviço: {e}")
        # Retorna um erro que o GraphQL pode mostrar ao cliente.
        return {"error": "Não foi possível conectar ao serviço de contatos."}


@mutation.field("adicionarContato")
def resolve_adicionar_contato(_, info, nome, categoria, telefones=None):
    """Resolve a mutation que cria um novo contato."""
    try:

        payload = {
            "nome": nome,
            "categoria": categoria,
            "telefones": telefones or []
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(CONTATOS_API_URL, json=payload, headers=headers)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar contato no microsserviço: {e} - {response.text}")
        return None


# Criando o schema executável
schema = make_executable_schema(type_defs, query, mutation)

# Criando o app FastAPI
app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montando o app GraphQL
graphql_app = GraphQL(schema, debug=True)
app.mount("/graphql", graphql_app)
