# gateway-graphql/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY..

# A porta que o Uvicorn (servidor ASGI para Ariadne) vai usar
EXPOSE 8000

# Comando para rodar a aplicação GraphQL com Uvicorn
# app:app refere-se ao objeto 'app' no arquivo 'app.py'
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
