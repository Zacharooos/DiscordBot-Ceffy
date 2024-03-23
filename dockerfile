# Use a imagem oficial do Python
FROM python:3.9-alpine

# Criar o diretório de destino para a aplicação
RUN mkdir -p /app

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos da aplicação para o diretório de trabalho
COPY . /app

# Instalar as dependências da aplicação
ENV CFLAGS="-O2"
RUN apk add --no-cache build-base
RUN apk add --no-cache poppler-utils ffmpeg
RUN apk add --no-cache opus
RUN pip install --upgrade pip && \
    apk add --update alpine-sdk && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base gcc python3-dev musl-dev libffi-dev && \
    pip install -r requirements.txt && \
    apk del .tmp-build-deps

# Adiniocar variavel de ambiente GOOGLE_API_KEY
# ARG GOOGLE_API_KEY=[api_key]

# Configurar o comando de inicialização da aplicação
CMD ["python3", "/app/src/main.py"]

# Comando para build em ARM64:
# docker buildx build --platform linux/arm64/v8 -t myimage:arm64v8 .
