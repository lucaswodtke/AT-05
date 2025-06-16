# scripts-teste/testar_consulta.py
import requests
import json
import sys

GRAPHQL_URL = "http://localhost:8000/graphql"

def consultar_contato_por_id(contato_id: str):
    print(f"--- Teste de Consulta do Contato ID: {contato_id} ---")
    
    query = """
    query ConsultarContato($id: ID!) {
        contato(id: $id) {
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
    variables = {"id": contato_id}
    
    try:
        response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables})
        response.raise_for_status()
        
        resultado = response.json()
        
        if "errors" in resultado:
            print(f"Erro ao consultar contato {contato_id} (GraphQL):")
            for error in resultado["errors"]:
                print(f"- {error['message']}")
        elif "data" in resultado and "contato" in resultado["data"]:
            contato_consultado = resultado["data"]["contato"]
            if contato_consultado:
                print("Contato encontrado:")
                print(json.dumps(contato_consultado, indent=2, ensure_ascii=False))
            else:
                print(f"Contato com ID {contato_id} não encontrado.")
        else:
            print("Resposta inesperada do servidor:", resultado)
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar consultar contato: {e}")
    except json.JSONDecodeError:
        print(f"Não foi possível decodificar a resposta JSON: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        id_para_consultar = sys.argv[1]
        consultar_contato_por_id(id_para_consultar)
    else:
        print("Por favor, forneça o ID do contato como argumento.")
        print("Exemplo de uso: python testar_consulta.py <ID_DO_CONTATO>")
        print("Dica: Execute 'testar_inclusao.py' primeiro para obter um ID válido.")
