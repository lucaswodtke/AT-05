from typing import List, Dict, Any
from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
import requests
import os

CONTATOS_API_URL = os.getenv("CONTATOS_API_URL", "http://localhost:5001/contatos")

query = QueryType()
mutation = MutationType()

@query.field("contatos")
def resolve_contatos(_, info) -> List[Dict[str, Any]]:
    try:
        response = requests.get(CONTATOS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar contatos: {e}")
        return []

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

@mutation.field("adicionarContato")
def resolve_adicionar_contato(_, info, nome: str, categoria: str, telefones: List[Dict[str, Any]] | None = None) -> Dict[str, Any] | None:
    payload = {
        "nome": nome,
        "categoria": categoria
    }
    if telefones:
        payload["telefones"] = [{"numero": t["numero"], "tipo": t["tipo"]} for t in telefones]

    try:
        response = requests.post(CONTATOS_API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao adicionar contato: {e}")
        return None

type_defs = """
    scalar ID

    type Telefone {
        numero: String!
        tipo: String!
    }

    type Contato {
        id: ID!
        nome: String!
        telefones: [Telefone!]
        categoria: String!
    }

    type Query {
        contatos: [Contato!]
        contato(id: ID!): Contato
    }

    input TelefoneInput {
        numero: String!
        tipo: String!
    }

    type Mutation {
        adicionarContato(
            nome: String!,
            telefones: [TelefoneInput!],
            categoria: String!
        ): Contato
    }
"""

schema = make_executable_schema(type_defs, query, mutation)
app = GraphQL(schema, debug=True)
