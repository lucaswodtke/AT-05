# scripts-teste/testar_listagem.py
import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def listar_todos_contatos():
    print("--- Teste de Listagem de Contatos ---")
    
    query = """
    query ListarContatos {
        contatos {
            id
            nome
            categoria
            telefones {
                numero
                tipo
            }
        }
    }
    """
    
    try:
        response = requests.post(GRAPHQL_URL, json={'query': query})
        response.raise_for_status()
        
        resultado = response.json()
        
        if "errors" in resultado:
            print("Erro ao listar contatos (GraphQL):")
            for error in resultado["errors"]:
                print(f"- {error['message']}")
        elif "data" in resultado and "contatos" in resultado["data"]:
            lista_de_contatos = resultado["data"]["contatos"]
            if lista_de_contatos:
                print("Contatos cadastrados:")
                print(json.dumps(lista_de_contatos, indent=2, ensure_ascii=False))
            else:
                print("Nenhum contato cadastrado encontrado.")
        else:
            print("Resposta inesperada do servidor:", resultado)

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar listar contatos: {e}")
    except json.JSONDecodeError:
        print(f"Não foi possível decodificar a resposta JSON: {response.text}")

if __name__ == "__main__":
    listar_todos_contatos()
