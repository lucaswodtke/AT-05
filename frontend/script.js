// frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const GRAPHQL_ENDPOINT = 'http://localhost:8000/graphql';

    const formAdicionarContato = document.getElementById('formAdicionarContato');
    const listaContatosUl = document.getElementById('listaContatos');
    const btnAtualizarLista = document.getElementById('btnAtualizarLista');
    const mensagemStatus = document.getElementById('mensagemStatus');
    const btnAdicionarTelefone = document.getElementById('btnAdicionarTelefone');
    const telefonesContainer = document.getElementById('telefonesContainer');
    let telefoneCount = 0;

    async function fetchGraphQL(query, variables = {}) {
        try {
            const response = await fetch(GRAPHQL_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, variables })
            });
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            const jsonResponse = await response.json();
            if (jsonResponse.errors) {
                throw new Error(jsonResponse.errors.map(e => e.message).join('\n'));
            }
            return jsonResponse.data;
        } catch (error) {
            mensagemStatus.textContent = `Erro: ${error.message}`;
            mensagemStatus.style.color = '#d9534f';
            console.error("Erro na requisição GraphQL:", error);
            throw error;
        }
    }

    async function carregarContatos() {
        const query = `
            query {
                contatos {
                    id
                    nome
                    categoria
                    telefones { numero tipo }
                }
            }
        `;
        try {
            const data = await fetchGraphQL(query);
            listaContatosUl.innerHTML = '';
            if (data && data.contatos && data.contatos.length > 0) {
                data.contatos.forEach(contato => {
                    const li = document.createElement('li');
                    let telefonesStr = "Sem telefones";
                    if (contato.telefones && contato.telefones.length > 0) {
                        telefonesStr = contato.telefones.map(t => `${t.numero} (${t.tipo})`).join(', ');
                    }
                    li.innerHTML = `<strong>${contato.nome}</strong> (Cat: ${contato.categoria}) <br> <small>Telefones: ${telefonesStr}</small>`;
                    listaContatosUl.appendChild(li);
                });
            } else {
                listaContatosUl.innerHTML = '<li>Nenhum contato cadastrado.</li>';
            }
            mensagemStatus.textContent = 'Lista de contatos atualizada.';
            mensagemStatus.style.color = '#3c763d';
        } catch (error) {
            // A mensagem de erro já é tratada em fetchGraphQL
        }
    }

    formAdicionarContato.addEventListener('submit', async (event) => {
        event.preventDefault();
        const nome = document.getElementById('nome').value;
        const categoria = document.getElementById('categoria').value;
        
        const telefonesInputs =;
        document.querySelectorAll('.telefone-entry').forEach(entry => {
            const numero = entry.querySelector('input[name^="telefoneNumero"]').value;
            const tipo = entry.querySelector('select').value;
            if (numero && tipo) {
                telefonesInputs.push({ numero, tipo: tipo.toUpperCase() });
            }
        });

        const mutation = `
            mutation AdicionarContato($nome: String!, $categoria: String!, $telefones:) {
                adicionarContato(nome: $nome, categoria: $categoria, telefones: $telefones) {
                    id
                    nome
                }
            }
        `;
        const variables = { nome, categoria: categoria.toUpperCase(), telefones: telefonesInputs };

        try {
            const data = await fetchGraphQL(mutation, variables);
            if (data && data.adicionarContato) {
                mensagemStatus.textContent = `Contato "${data.adicionarContato.nome}" adicionado com sucesso!`;
                mensagemStatus.style.color = '#3c763d';
                formAdicionarContato.reset();
                document.querySelectorAll('.telefone-entry').forEach(entry => entry.remove());
                telefoneCount = 0;
                carregarContatos();
            }
        } catch (error) {
            // A mensagem de erro já é tratada em fetchGraphQL
        }
    });

    btnAdicionarTelefone.addEventListener('click', () => {
        telefoneCount++;
        const div = document.createElement('div');
        div.classList.add('telefone-entry');
        div.innerHTML = `
            <label for="telefoneNumero${telefoneCount}">Número:</label>
            <input type="text" id="telefoneNumero${telefoneCount}" name="telefoneNumero${telefoneCount}" required>
            <label for="telefoneTipo${telefoneCount}">Tipo:</label>
            <select id="telefoneTipo${telefoneCount}" name="telefoneTipo${telefoneCount}">
                <option value="MOVEL">Móvel</option>
                <option value="FIXO">Fixo</option>
                <option value="COMERCIAL">Comercial</option>
            </select>
            <button type="button" class="btnRemoverTelefone">Remover</button>
        `;
        telefonesContainer.insertBefore(div, btnAdicionarTelefone);

        div.querySelector('.btnRemoverTelefone').addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    btnAtualizarLista.addEventListener('click', carregarContatos);

    carregarContatos();
});
