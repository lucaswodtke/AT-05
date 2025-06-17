# frontend/Dockerfile

# Usar uma imagem base oficial do Nginx
FROM nginx:alpine

# Copiar os arquivos estáticos do frontend para o diretório padrão do Nginx
COPY . /usr/share/nginx/html

# Expor a porta 80 (padrão do Nginx)
EXPOSE 80

# O comando padrão do Nginx já é para iniciar o servidor
CMD ["nginx", "-g", "daemon off;"]
