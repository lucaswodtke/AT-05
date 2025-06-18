# Projeto Agenda de Contatos com Microsserviços

## Descrição

Este projeto implementa uma aplicação de Agenda de Contatos, utilizando uma arquitetura de microsserviços. O objetivo é demonstrar a criação de uma API REST para gerenciar os dados, a exposição dessa API através de um Gateway GraphQL, e a orquestração de todos os serviços de forma isolada utilizando Docker.

A aplicação permite que um usuário adicione, liste e consulte contatos através de uma interface web simples que se comunica com o backend.

## Arquitetura

O projeto é dividido em três serviços principais que se comunicam em um ambiente containerizado:

`Frontend (Nginx)` --\> `Gateway GraphQL (FastAPI)` --\> `Microsserviço Contatos (Flask)`

## Tecnologias Utilizadas

  * **Linguagem (Backend):** Python 3.9
  * **Microsserviço REST:** Flask
  * **Gateway GraphQL:** FastAPI, Ariadne, Uvicorn
  * **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
  * **Conteinerização:** Docker, Docker Compose

## Pré-requisitos

  * **Windows 11** com WSL 2 (Subsistema do Windows para Linux) ativado.
  * **Docker Desktop para Windows** instalado e em execução.
      * *Verifique se o Docker Desktop está usando o backend WSL 2 para melhor performance.*
  * **Windows Terminal** (ou qualquer outro terminal como PowerShell/CMD).

## Estrutura de Diretórios

```
AT-05/
├── docker-compose.yml
├── README.md
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── script.js
│   └── style.css
├── gateway-graphql/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── microsservico-contatos/
│   ├── Dockerfile
│   ├── app.py
│   ├── models.py
│   └── requirements.txt
└── scripts-teste/
    ├── testar_consulta.py
    ├── testar_inclusao.py
    └── testar_listagem.py
```

## Como Executar a Aplicação (Passo a Passo no Windows 11)

### 1\. Instale o Docker Desktop

  * Baixe o instalador oficial em: **[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)**
  * Execute o instalador e siga as instruções. É altamente recomendável habilitar a integração com WSL 2 durante a instalação.
  * Após a instalação, reinicie o computador se solicitado.
  * Abra o **Docker Desktop** e aguarde até que o ícone da baleia na barra de tarefas fique estável (sem a animação de "starting").

### 2\. Obtenha os Arquivos do Projeto

  * Clone o repositório ou baixe e descompacte os arquivos do projeto em uma pasta de fácil acesso. Por exemplo, na sua Área de Trabalho dentro de uma pasta chamada `AT-05`.
  * O caminho seria algo como: `C:\Users\SeuUsuario\Desktop\AT-05`

### 3\. Abra o Terminal e Navegue até a Pasta do Projeto

  * Abra o **Windows Terminal** (ou PowerShell).
  * Use o comando `cd` para navegar até o diretório onde você salvou o projeto. **Atenção:** Substitua `SeuUsuario` pelo seu nome de usuário real do Windows.

<!-- end list -->

```powershell
cd C:\Users\SeuUsuario\Desktop\AT-05
```

### 4\. Inicie Todos os Serviços

  * Com o Terminal aberto na pasta raiz do projeto, execute o seguinte comando:

<!-- end list -->

```powershell
docker-compose up --build
```

  * Este comando fará o seguinte:
      * `--build`: Força a construção das imagens Docker do zero, garantindo que todas as alterações nos arquivos sejam aplicadas.
      * `up`: Inicia todos os serviços definidos no arquivo `docker-compose.yml`.
  * Aguarde o processo terminar. Você verá vários logs coloridos aparecendo, indicando que cada serviço (frontend, gateway, microsserviço) está sendo iniciado. **Não feche esta janela do Terminal**, pois ela mostra os logs em tempo real e mantém os serviços em execução.

### 5\. Acesse e Utilize a Aplicação

Com os serviços rodando, você pode acessar as diferentes partes da aplicação:

  * **Interface da Agenda:** Abra seu navegador (Chrome, Firefox, Edge) e acesse:

      * **`http://localhost:8080`**
      * Você verá a página da agenda de contatos. Tente adicionar um novo contato e veja a lista ser atualizada.

  * **Ambiente de Testes GraphQL (GraphiQL):** Para interagir diretamente com o Gateway, acesse:

      * **`http://localhost:8000/graphql`**
      * Esta é uma ferramenta para testar suas `queries` e `mutations` GraphQL.

  * **API REST (Direto no Microsserviço):** Para ver o JSON puro retornado pelo microsserviço, acesse:

      * **`http://localhost:5001/contatos`**

## Como Testar a API (Via Scripts)

### Testando com os Scripts

Para testar as funcionalidades da API REST diretamente via scripts:

1.  Abra um **novo Terminal** (deixe o primeiro rodando o `docker-compose`).
2.  Navegue novamente para a pasta do projeto: `cd C:\Users\SeuUsuario\Desktop\AT-05\scripts-teste`.
3.  Execute os scripts de teste um por um:

<!-- end list -->

```powershell
# Para adicionar um contato de teste
python testar_inclusao.py

# Para listar todos os contatos (incluindo o que você acabou de adicionar)
python testar_listagem.py

# Para testar a consulta de um contato específico
python testar_consulta.py
```

### Testando com a Interface GraphiQL

1.  Acesse **`http://localhost:8000/graphql`**.

2.  No painel da esquerda, você pode escrever consultas.

    **Exemplo de Query (para listar contatos):**

    ```graphql
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
    ```

    **Exemplo de Mutation (para adicionar um contato):**

    ```graphql
    mutation {
      adicionarContato(
        nome: "Contato via GraphQL",
        categoria: PESSOAL,
        telefones: [
          {numero: "12345-6789", tipo: MOVEL}
        ]
      ) {
        id
        nome
      }
    }
    ```

3.  Pressione o botão de "Play" (▶) para executar a operação.

## Como Parar a Aplicação

1.  Volte para o primeiro Terminal (onde você executou o `docker-compose up`).
2.  Pressione as teclas `Ctrl` + `C` para parar a execução dos serviços.
3.  Para remover os contêineres e a rede criada, liberando os recursos, execute:
    ```powershell
    docker-compose down
    ```

## Autor

  * **Lucas Henrique Gonçalves Wodtke**

-----

-----

# Relatório de Desenvolvimento: API de Microsserviços para Agenda de Contatos

## 1\. Introdução

Este relatório detalha o processo de desenvolvimento da aplicação de Agenda de Contatos, construída com base em uma arquitetura de microsserviços. O objetivo principal foi demonstrar a criação de uma API REST para gerenciar contatos, a exposição dessa API através de um gateway GraphQL, o desenvolvimento de uma interface de frontend simples para interação do usuário, e a conteinerização de todos os componentes para garantir um ambiente de execução isolado e consistente.

Este documento está estruturado da seguinte forma: Visão Geral da Arquitetura, Desenvolvimento dos Microsserviços, Desenvolvimento do Frontend, Conteinerização, Configuração e Execução, Testes, Estrutura de Arquivos e Conclusão.

## 2\. Visão Geral da Arquitetura

Para atender aos requisitos da tarefa, foi definida uma arquitetura baseada em microsserviços, composta por três componentes principais:

  * **Microsserviço de Contatos (API REST):** O núcleo da aplicação, responsável por toda a lógica de negócio relacionada aos contatos (inclusão, consulta, listagem). Ele expõe suas funcionalidades através de uma API RESTful.
  * **Gateway GraphQL:** Atua como uma fachada única para os clientes. Ele recebe requisições GraphQL, traduz e as direciona para o microsserviço de Contatos. Isso simplifica o acesso aos dados para o frontend, permitindo que ele solicite apenas as informações necessárias em uma única requisição.
  * **Frontend:** Uma interface web simples que permite aos usuários interagir com a agenda. Ele se comunica exclusivamente com o Gateway GraphQL, desconhecendo a existência do microsserviço REST.

Abaixo, um diagrama conceitual da arquitetura:

### Tecnologias Utilizadas:

  * **Linguagem de Programação (Backend):** Python 3.9.
  * **Microsserviço de Contatos (API REST):**
      * **Framework:** Flask. Escolhido por sua simplicidade e baixo acoplamento, ideal para criar APIs RESTful rapidamente.
  * **Gateway GraphQL:**
      * **Framework:** FastAPI. Um framework moderno e de alta performance, com excelente suporte a programação assíncrona.
      * **Biblioteca GraphQL:** Ariadne. Uma biblioteca *schema-first* que se integra perfeitamente com FastAPI.
      * **Servidor ASGI:** Uvicorn.
  * **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS).
  * **Conteinerização:** Docker e Docker Compose.

## 3\. Desenvolvimento dos Microsserviços

### 3.1. Microsserviço de Contatos (API REST)

Este serviço é a fonte da verdade para os dados dos contatos.

  * **Responsabilidades:** Inclusão, consulta por ID e listagem de todos os contatos.
  * **Estrutura de Dados:** Utiliza classes Python e `Enum` para representar Contatos, Telefones, Tipos de Telefone e Categorias, garantindo consistência. Os dados são mantidos em uma estrutura em memória para simplificar (um dicionário Python).
  * **Endpoints REST:**
      * `POST /contatos`: Cria um novo contato.
      * `GET /contatos`: Lista todos os contatos.
      * `GET /contatos/{contato_id}`: Consulta um contato específico.

### 3.2. Gateway GraphQL

O Gateway desacopla o frontend do backend, oferecendo uma API flexível.

  * **Responsabilidades:** Expor um schema GraphQL, resolver `queries` e `mutations` e delegar a lógica para a API REST de Contatos.

  * **Schema GraphQL:** O schema define os tipos, consultas e mutações disponíveis. Foi definido usando a sintaxe SDL (Schema Definition Language) do GraphQL.

    ```graphql
    enum Categoria { FAMILIAR, PESSOAL, COMERCIAL }
    enum TipoTelefone { MOVEL, FIXO, COMERCIAL }

    type Telefone {
      numero: String!
      tipo: TipoTelefone!
    }

    input TelefoneInput {
      numero: String!
      tipo: TipoTelefone!
    }

    type Contato {
      id: ID!
      nome: String!
      categoria: Categoria!
      telefones: [Telefone!]
    }

    type Query {
      contatos: [Contato!]
    }

    type Mutation {
      adicionarContato(
        nome: String!,
        categoria: Categoria!,
        telefones: [TelefoneInput!]
      ): Contato
    }
    ```

## 4\. Desenvolvimento do Frontend

O frontend é uma Single Page Application (SPA) minimalista para demonstrar o consumo da API.

  * **Funcionalidades:** Listar os contatos existentes ao carregar a página e fornecer um formulário para adicionar novos contatos.
  * **Tecnologias:** HTML, CSS e JavaScript puro, utilizando a API `fetch` para realizar chamadas GraphQL para o gateway.

## 5\. Conteinerização com Docker e Docker Compose

A conteinerização para garantir o isolamento e a portabilidade do projeto.

  * **Dockerfile:** Cada serviço (`microsservico-contatos`, `gateway-graphql` e `frontend`) possui seu próprio `Dockerfile`. Ele descreve os passos para construir uma imagem autocontida do serviço, incluindo a instalação de dependências e a definição do comando de inicialização.
  * **Docker Compose:** O arquivo `docker-compose.yml` orquestra todos os containers. Ele define os serviços, como construí-los, as portas a serem expostas, as variáveis de ambiente e a rede interna (`agenda-net`) para que os containers possam se comunicar usando seus nomes de serviço.

## 6\. Configuração e Execução do Projeto

O projeto foi configurado para ser iniciado com um único comando (`docker-compose up --build`), o que simplificando o processo de setup do ambiente de desenvolvimento. As instruções detalhadas estão na seção "Como Executar a Aplicação" no início deste documento.

## 7\. Testando as Operações

A validação das funcionalidades foi realizada de três formas:

1.  **Manualmente via Frontend:** Interagindo com a interface web em `http://localhost:8080`.
2.  **Manualmente via Gateway:** Utilizando a interface GraphiQL em `http://localhost:8000/graphql` para enviar `queries` e `mutations`.
3.  **Via Scripts Automatizados:** Executando os scripts na pasta `scripts-teste/` para validar programaticamente os endpoints da API REST.

## 8\. Estrutura de Arquivos Detalhada

| Caminho do Arquivo/Pasta   | Finalidade Resumida                                                 |
| -------------------------- | ------------------------------------------------------------------- |
| `AT-05/`                   | Diretório raiz do projeto.                                          |
| `microsservico-contatos/`  | Contém os arquivos da API REST de Contatos (Flask).                 |
| `gateway-graphql/`         | Contém os arquivos do Gateway GraphQL (FastAPI + Ariadne).          |
| `frontend/`                | Contém os arquivos da interface do usuário (HTML/CSS/JS).           |
| `scripts-teste/`           | Contém scripts Python para testes da API REST.                      |
| `docker-compose.yml`       | Arquivo de configuração do Docker Compose para orquestrar os serviços. |
| `README.md`                | Este arquivo, com a descrição e instruções do projeto.              |

## 9\. Conclusão

Este projeto demonstrou a implementação de uma arquitetura de microsserviços para uma aplicação simples. Foram abordados conceitos chave como criação de APIs REST, implementação de um Gateway GraphQL, desenvolvimento de um frontend consumidor e a orquestração de todos os componentes com Docker. A abordagem adotada resulta em um sistema modular, escalável e de fácil manutenção.

### Possíveis Evoluções e Melhorias:

  * **Persistência de Dados:** Substituir o armazenamento em memória por um banco de dados real (como PostgreSQL ou MongoDB), executando em seu próprio container.
  * **Autenticação e Autorização:** Implementar um serviço de autenticação (e.g., com JWT) para proteger a API.
  * **Testes Abrangentes:** Expandir a suíte de testes para incluir testes unitários e de integração mais robustos.
  * **Validação de Dados:** Adicionar validação de entrada mais rigorosa nos endpoints da API e no gateway.
  * **CI/CD:** Configurar um pipeline de Integração Contínua e Entrega Contínua para automatizar testes e deploys.

## 10\. Referências

  * **Python:** [https://docs.python.org/pt-br/3/](https://docs.python.org/pt-br/3/)
  * **Flask:** [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
  * **FastAPI:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
  * **Ariadne:** [https://ariadnegraphql.org/](https://ariadnegraphql.org/)
  * **GraphQL:** [https://graphql.org/learn/](https://graphql.org/learn/)
  * **Docker:** [https://docs.docker.com/](https://docs.docker.com/)
