# microsservico-contatos/Dockerfile

# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY ./requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que a aplicação Flask vai usar (deve ser a mesma usada no app.py)
EXPOSE 5001

# Comando para executar a aplicação quando o container iniciar
CMD ["python", "app.py"]
