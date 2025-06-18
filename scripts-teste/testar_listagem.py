import requests
import json

# URL base da API do microsserviço de contatos
API_URL = "http://localhost:5001/contatos"

def testar_listagem_contatos():
    """
    Testa a funcionalidade de listagem de todos os contatos da API.
    """
    print("--- Teste: Listagem de Contatos ---")

    try:
        # Realiza a requisição GET para o endpoint /contatos
        response = requests.get(API_URL)
        
        print(f"Status Code: {response.status_code}")
        
        # A API deve retornar 200 (OK) em caso de sucesso
        if response.status_code == 200:
            contatos = response.json()
            print(f"Total de contatos encontrados: {len(contatos)}")
            print("Lista de Contatos:")
            print(json.dumps(contatos, indent=2, ensure_ascii=False))
            print("\n>> SUCESSO: Listagem de contatos funcionando corretamente!")
        else:
            print("Resposta de erro da API:")
            print(response.text)
            print("\n>> FALHA: Não foi possível listar os contatos.")

    except requests.exceptions.RequestException as e:
        print(f"\n>> ERRO DE CONEXÃO: Não foi possível conectar à API em {API_URL}.")
        print(f"   Certifique-se de que os contêineres Docker estão em execução.")
        print(f"   Erro: {e}")

if __name__ == "__main__":
    testar_listagem_contatos()
