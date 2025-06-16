
# Projeto Agenda de Contatos com Microsserviços

## Descrição
Este projeto implementa uma aplicação completa de Agenda de Contatos, utilizando uma arquitetura de microsserviços. O objetivo é demonstrar a criação de uma API REST para gerenciar os dados, a exposição dessa API através de um Gateway GraphQL, e a orquestração de todos os serviços de forma isolada utilizando Docker.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Plataforma:** Windows 11
- **Microsserviço REST:** Flask
- **Gateway GraphQL:** Ariadne, Uvicorn
- **Frontend:** HTML, CSS, JavaScript
- **Conteinerização:** Docker, Docker Compose

## Pré-requisitos
1. Docker Desktop instalado no Windows 11

## Instalação e Configuração
1. **Instale o Docker Desktop**
    - Baixe o instalador oficial em: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
    - Execute o instalador e siga as instruções. Se for solicitado, reinicie o computador.
    - Abra o Docker Desktop e aguarde o ícone da baleia na barra de tarefas ficar estável.

2. **Obtenha os arquivos do projeto**
    - Crie uma pasta na sua **Área de Trabalho** chamada `AT-05`.
    - Coloque todas as pastas e arquivos do projeto dentro dela.

3. **Abra o Terminal e navegue até a pasta do projeto**
    > **Atenção:** Substitua `SeuUsuario` pelo seu nome de usuário real do Windows.powershell
    cd C:\Users\SeuUsuario\Desktop\AT-05
    ```

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

## Como Executar a Aplicação
1. **Inicie todos os serviços**
    - Com o Terminal aberto na pasta do projeto, execute o comando:
    ```powershell
    docker-compose up --build
    ```
    - Aguarde o processo terminar. Você verá vários logs coloridos aparecendo. Não feche esta janela do Terminal.

2. **Acesse a aplicação**
    - Abra seu navegador e acesse a seguinte URL:
    ```
    http://localhost:8080
    ```

3. **Como testar a API (Opcional)**
    - Para testar as funcionalidades via script, abra um **novo Terminal**, navegue até a pasta do projeto e execute:
    ```powershell
    # Adicionar um contato de teste
    python.\scripts-teste\testar_inclusao.py
    
    # Listar todos os contatos
    python.\scripts-teste\testar_listagem.py
    ```

4. **Como parar a aplicação**
    - Volte para o primeiro Terminal (onde você executou o `docker-compose up`).
    - Pressione as teclas **Ctrl + C**.
    - Para remover os contêineres e limpar o ambiente, execute:
    ```powershell
    docker-compose down
    ```

## Autor
Lucas Henrique Gonçalves Wodtke
```
