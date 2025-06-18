import requests
import json
import sys

# URL base da API do microsserviço de contatos
API_URL = "http://localhost:5001/contatos"

def criar_contato_para_teste():
    """Cria um contato temporário e retorna seu ID."""
    contato_teste = {
        "nome": "Contato de Consulta",
        "telefones": [{"numero": "1111-1111", "tipo": "FIXO"}],
        "categoria": "PESSOAL"
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, data=json.dumps(contato_teste), headers=headers)
        if response.status_code == 201:
            return response.json().get("id")
        return None
    except requests.exceptions.RequestException:
        return None

def testar_consulta_contato():
    """
    Testa a funcionalidade de consulta de um contato específico pelo ID.
    """
    print("--- Teste: Consulta de Contato Específico ---")
    
    print("1. Criando um contato de teste para obter um ID válido...")
    contato_id = criar_contato_para_teste()

    if not contato_id:
        print("\n>> FALHA CRÍTICA: Não foi possível criar o contato inicial para o teste.")
        print("   Verifique se o endpoint de inclusão está funcionando e se a API está online.")
        sys.exit(1) # Encerra o script se não puder criar o contato

    print(f"   Contato criado com sucesso! ID: {contato_id}")
    
    print("\n2. Testando a consulta do contato recém-criado...")
    try:
        # Constrói a URL para a consulta específica
        url_consulta = f"{API_URL}/{contato_id}"
        response = requests.get(url_consulta)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   Contato encontrado:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            print("\n   >> SUCESSO: Consulta de contato existente funciona!")
        else:
            print("   >> FALHA: Não foi possível consultar o contato criado.")

    except requests.exceptions.RequestException as e:
         print(f"\n>> ERRO DE CONEXÃO: {e}")

    print("\n3. Testando a consulta de um contato com ID inválido...")
    try:
        url_invalida = f"{API_URL}/id-que-nao-existe-123"
        response = requests.get(url_invalida)
        
        print(f"   Status Code para ID inválido: {response.status_code}")
        if response.status_code == 404:
            print("   >> SUCESSO: API retornou '404 Not Found' como esperado para um ID inválido.")
        else:
            print("   >> FALHA: API não retornou 404 para um ID inválido.")

    except requests.exceptions.RequestException as e:
         print(f"\n>> ERRO DE CONEXÃO: {e}")


if __name__ == "__main__":
    testar_consulta_contato()
