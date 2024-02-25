# Use uma imagem Python mais leve
FROM python:3.11-slim

LABEL maintainer="Marcos Vinícius (droid-M)"

# Instala o pacote kbd para permitir o uso da biblioteca keyboard
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        kbd \
    && rm -rf /var/lib/apt/lists/*

# Configura o diretório de trabalho
WORKDIR /app

# Configura o ambiente
COPY src/ /app

# Adiciona um diretório para persistir dados
VOLUME /app/data

RUN pip install -r /app/requirements.txt

CMD ["python", "main.py"]
