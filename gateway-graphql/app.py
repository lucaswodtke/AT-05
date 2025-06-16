# gateway-graphql/app.py
from typing import List, Dict, Any
from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
import requests
import os

# URL do microsserviço de contatos.
# Quando rodando com Docker Compose, usaremos o nome do serviço.
CONTATOS_API_URL = os.getenv("CONTATOS_API_URL", "http://localhost:5001/contatos")

# Definindo os tipos do schema
query = QueryType()
mutation = MutationType()

# Resolvers para Query
@query.field("contatos")
def resolve_contatos(_, info) -> List]:
    try:
        response = requests.get(f"{CONTATOS_API_URL}")
        response.raise_for_status() # Lança exceção para erros HTTP (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar contatos: {e}")
        return # Retorna lista vazia em caso de erro

@query.field("contato")
def resolve_contato(_, info, id: str) -> Dict[str, Any] | None:
    try:
        response = requests.get(f"{CONTATOS_API_URL}/{id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar contato {id}: {e}")
        return None

# Resolvers para Mutation
@mutation.field("adicionarContato")
def resolve_adicionar_contato(_, info, nome: str, categoria: str, telefones: List] = None) -> Dict[str, Any] | None:
    payload = {
        "nome": nome,
        "categoria": categoria.lower(), # API REST espera minúsculas para enums
        "telefones":
    }
    if telefones:
        payload["telefones"] = [{"numero": t["numero"], "tipo": t["tipo"].lower()} for t in telefones]
    
    try:
        response = requests.post(CONTATOS_API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar contato: {e}")
        # Poderia levantar uma exceção GraphQL aqui para melhor feedback ao cliente
        return None

# Definição do Schema GraphQL (SDL)
type_defs = """
    scalar ID

    type Telefone {
        numero: String!
        tipo: String!
    }

    type Contato {
        id: ID!
        nome: String!
        telefones:
        categoria: String!
    }

    type Query {
        contatos: [Contato!]
        contato(id: ID!): Contato
    }

    input TelefoneInput {
        numero: String!
        tipo: String! # Idealmente um Enum: MOVEL, FIXO, COMERCIAL
    }

    type Mutation {
        adicionarContato(
            nome: String!,
            telefones:, # Lista de telefones
            categoria: String! # Idealmente um Enum: FAMILIAR, PESSOAL, COMERCIAL
        ): Contato
    }
"""

schema = make_executable_schema(type_defs, query, mutation)
app = GraphQL(schema, debug=True) # Aplicação ASGI
