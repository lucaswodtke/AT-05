# scripts-teste/testar_inclusao.py
import requests
import json

GRAPHQL_URL = "http://localhost:8000/graphql"

def adicionar_novo_contato():
    print("--- Teste de Inclusão de Contato ---")
    
    mutation = """
    mutation AdicionarNovoContato($nome: String!, $categoria: String!, $telefones:) {
        adicionarContato(nome: $nome, categoria: $categoria, telefones: $telefones) {
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
    
    variables = {
        "nome": "Maria Silva (Teste via Script)",
        "categoria": "PESSOAL",
        "telefones": [
            {"numero": "91234-5678", "tipo": "MOVEL"},
            {"numero": "3322-1100", "tipo": "FIXO"}
        ]
    }
    
    try:
        response = requests.post(GRAPHQL_URL, json={'query': mutation, 'variables': variables})
        response.raise_for_status() # Lança exceção para erros HTTP
        
        resultado = response.json()
        
        if "errors" in resultado:
            print("Erro ao adicionar contato (GraphQL):")
            for error in resultado["errors"]:
                print(f"- {error['message']}")
        elif "data" in resultado and resultado["data"]["adicionarContato"]:
            contato_adicionado = resultado["data"]["adicionarContato"]
            print("Contato adicionado com sucesso:")
            print(json.dumps(contato_adicionado, indent=2, ensure_ascii=False))
            return contato_adicionado["id"] # Retorna o ID para uso em outros testes
        else:
            print("Resposta inesperada do servidor:", resultado)
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar adicionar contato: {e}")
    except json.JSONDecodeError:
        print(f"Não foi possível decodificar a resposta JSON: {response.text}")
    return None

if __name__ == "__main__":
    id_novo_contato = adicionar_novo_contato()
    if id_novo_contato:
        print(f"\nID do contato adicionado para consulta: {id_novo_contato}")
