# microsservico-contatos/app.py
from flask import Flask, request, jsonify
from models import Contato, Telefone, TipoTelefone, CategoriaContato, banco_de_dados_contatos

app = Flask(__name__)

@app.route('/contatos', methods=)
def adicionar_contato_api():
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'categoria' not in dados:
        return jsonify({"erro": "Dados incompletos"}), 400

    try:
        nome = dados['nome']
        # Converte string da categoria para o enum CategoriaContato
        categoria_str = dados['categoria'].upper()
        categoria = CategoriaContato[categoria_str]
        
        novo_contato = Contato(nome=nome, categoria=categoria)

        if 'telefones' in dados and isinstance(dados['telefones'], list):
            for tel_data in dados['telefones']:
                # Converte string do tipo para o enum TipoTelefone
                tipo_tel_str = tel_data['tipo'].upper()
                tipo_tel = TipoTelefone[tipo_tel_str]
                telefone = Telefone(numero=tel_data['numero'], tipo=tipo_tel)
                novo_contato.adicionar_telefone(telefone)
        
        banco_de_dados_contatos[novo_contato.id] = novo_contato
        return jsonify(novo_contato.to_dict()), 201
    except (KeyError, ValueError) as e: # Captura erros de chave não encontrada no enum ou valor inválido
        return jsonify({"erro": f"Erro nos dados de entrada: {str(e)}"}), 400

@app.route('/contatos/<string:contato_id>', methods=)
def consultar_contato_api(contato_id):
    contato = banco_de_dados_contatos.get(contato_id)
    if contato:
        return jsonify(contato.to_dict()), 200
    return jsonify({"erro": "Contato não encontrado"}), 404

@app.route('/contatos', methods=)
def listar_contatos_api():
    lista_contatos = [contato.to_dict() for contato in banco_de_dados_contatos.values()]
    return jsonify(lista_contatos), 200

if __name__ == '__main__':
    # Porta diferente da padrão para evitar conflitos, ex: 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
