from flask import Flask, request, jsonify
from models import Contato, Telefone, TipoTelefone, CategoriaContato, banco_de_dados_contatos

app = Flask(__name__)

@app.route('/contatos', methods=['GET', 'POST'])
def gerenciar_contatos():
    if request.method == 'POST':
        dados = request.get_json()
        if not dados or 'nome' not in dados or 'categoria' not in dados:
            return jsonify({"erro": "Dados incompletos"}), 400
        try:
            nome = dados['nome']
            categoria_str = dados['categoria'].upper()
            categoria = CategoriaContato[categoria_str]

            novo_contato = Contato(nome=nome, categoria=categoria)

            if 'telefones' in dados and isinstance(dados['telefones'], list):
                for tel_data in dados['telefones']:
                    tipo_tel_str = tel_data['tipo'].upper()
                    tipo_tel = TipoTelefone[tipo_tel_str]
                    telefone = Telefone(numero=tel_data['numero'], tipo=tipo_tel)
                    novo_contato.adicionar_telefone(telefone)

            banco_de_dados_contatos[novo_contato.id] = novo_contato
            return jsonify(novo_contato.to_dict()), 201

        except (KeyError, ValueError) as e:
            return jsonify({"erro": f"Erro nos dados de entrada: {str(e)}"}), 400

    else:  # GET
        lista_contatos = [contato.to_dict() for contato in banco_de_dados_contatos.values()]
        return jsonify(lista_contatos), 200

@app.route('/contatos/<string:contato_id>', methods=['GET'])
def consultar_contato_api(contato_id):
    contato = banco_de_dados_contatos.get(contato_id)
    if contato:
        return jsonify(contato.to_dict()), 200
    return jsonify({"erro": "Contato não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
