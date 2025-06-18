const endpointGraphQL = "http://localhost:8000/graphql";

const listaContatosDiv = document.getElementById("listaContatos");
const formContato = document.getElementById("formContato");
const telefonesContainer = document.getElementById("telefonesContainer");
const btnAddTelefone = document.getElementById("btnAddTelefone");

btnAddTelefone.addEventListener("click", () => {
    const div = document.createElement("div");
    div.classList.add("telefone");
    div.innerHTML = `
    <label>Número: <input type="text" class="numero" required></label>
    <label>Tipo:
        <select class="tipo" required>
        <option value="">Selecione</option>
        <option value="MOVEL">Móvel</option>
        <option value="FIXO">Fixo</option>
        <option value="COMERCIAL">Comercial</option>
        </select>
    </label>
    <button type="button" class="btnRemoveTelefone">Remover</button>
    `;
    telefonesContainer.appendChild(div);

    div.querySelector(".btnRemoveTelefone").addEventListener("click", () => {
        div.remove();
    });
});

async function listarContatos() {
    const query = `
        query {
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
    `;
    try {
        const res = await fetch(endpointGraphQL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await res.json();
        if (data.errors) {
            listaContatosDiv.innerText = "Erro ao buscar contatos.";
            console.error(JSON.stringify(data.errors, null, 2));
            return;
        }
        mostrarContatos(data.data.contatos);
    } catch (err) {
        listaContatosDiv.innerText = "Erro na comunicação com o servidor.";
        console.error(err);
    }
}

function mostrarContatos(contatos) {
    if (!contatos || contatos.length === 0) {
        listaContatosDiv.innerHTML = "<p>Nenhum contato cadastrado.</p>";
        return;
    }
    listaContatosDiv.innerHTML = "";
    contatos.forEach(c => {
        const div = document.createElement("div");
        div.classList.add("contato");
        const categoriaFormatada = c.categoria.charAt(0).toUpperCase() + c.categoria.slice(1).toLowerCase();
        
        div.innerHTML = `
            <strong>${c.nome}</strong> (<em>${categoriaFormatada}</em>)
            <div class="telefone-lista">
                Telefones:
                <ul>
                    ${c.telefones.map(t => {
                        const tipoFormatado = t.tipo.charAt(0).toUpperCase() + t.tipo.slice(1).toLowerCase();
                        return `<li>${tipoFormatado}: ${t.numero}</li>`
                    }).join("")}
                </ul>
            </div>
        `;
        listaContatosDiv.appendChild(div);
    });
}

formContato.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const categoria = document.getElementById("categoria").value;
    const telefoneElements = [...telefonesContainer.querySelectorAll(".telefone")];

    if (!nome || !categoria) {
        alert("Por favor, preencha nome e categoria.");
        return;
    }

    const telefones = telefoneElements.map(div => {
        return {
            numero: div.querySelector(".numero").value.trim(),
            tipo: div.querySelector(".tipo").value
        };
    }).filter(t => t.numero && t.tipo);
    
    const mutation = `
        mutation AdicionarContato($nome: String!, $categoria: Categoria!, $telefones: [TelefoneInput!]) {
            adicionarContato(nome: $nome, categoria: $categoria, telefones: $telefones) {
                id
                nome
            }
        }
    `;

    const variables = { nome, categoria, telefones };

    try {
        const res = await fetch(endpointGraphQL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: mutation, variables })
        });
        const data = await res.json();
        if (data.errors) {
            alert("Erro ao adicionar contato. Verifique o console para detalhes.");
            console.error(JSON.stringify(data.errors, null, 2));
            return;
        }
        alert("Contato adicionado com sucesso!");
        formContato.reset();
        // Limpa os campos de telefone dinâmicos
        telefonesContainer.innerHTML = "<h3>Telefones</h3>"; 
        listarContatos();
    } catch (err) {
        alert("Erro na comunicação com o servidor.");
        console.error(err);
    }
});

// Botão listar contatos
document.getElementById("btnListar").addEventListener("click", listarContatos);

// Inicializa listagem na abertura da página
listarContatos();
