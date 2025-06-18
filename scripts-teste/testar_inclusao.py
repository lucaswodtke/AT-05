import requests
import json

# URL base da API do microsserviço de contatos
API_URL = "http://localhost:5001/contatos"

def testar_inclusao_contato():
    """
    Testa a funcionalidade de inclusão de um novo contato na API.
    """
    print("--- Teste: Inclusão de Novo Contato ---")
    
    # Dados do novo contato que serão enviados no corpo da requisição
    # Note que os valores para 'categoria' e 'tipo' devem ser os NOMES dos enums (maiúsculos)
    novo_contato = {
        "nome": "Prof. Teste de Software",
        "telefones": [
            {"numero": "98765-4321", "tipo": "MOVEL"},
            {"numero": "3322-1100", "tipo": "COMERCIAL"}
        ],
        "categoria": "COMERCIAL"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Realiza a requisição POST para o endpoint /contatos
        response = requests.post(API_URL, data=json.dumps(novo_contato), headers=headers)
        
        # Imprime o status code da resposta HTTP
        print(f"Status Code: {response.status_code}")
        
        # A API deve retornar 201 (Created) em caso de sucesso
        if response.status_code == 201:
            print("Resposta da API (contato criado):")
            # Imprime o corpo da resposta formatado em JSON
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            print("\n>> SUCESSO: Contato incluído com êxito!")
        else:
            print("Resposta de erro da API:")
            print(response.text)
            print("\n>> FALHA: Não foi possível incluir o contato.")

    except requests.exceptions.RequestException as e:
        print(f"\n>> ERRO DE CONEXÃO: Não foi possível conectar à API em {API_URL}.")
        print(f"   Certifique-se de que os contêineres Docker estão em execução.")
        print(f"   Erro: {e}")

if __name__ == "__main__":
    testar_inclusao_contato()
