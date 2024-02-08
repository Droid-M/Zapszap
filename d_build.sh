#!/bin/bash

# Verifica se o número de argumentos é suficiente
if [ "$#" -lt 1 ]; then
    echo "Uso: $0 <ID>"
    exit 1
fi

# Nome, tag da imagem Docker
IMAGE_NAME="zap$1"
# IMAGE_TAG="$1"
IMAGE_TAG="1"
FOURTH_OCTET="$1"
EXTERNAL_PORT="905$1"

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker para continuar."
    exit 1
fi

# Verifica se a rede já existe
if ! docker network inspect zapnetwork &> /dev/null; then
    # Cria uma rede bridge personalizada com um IP específico
    docker network create --subnet=172.22.0.0/16 zapnetwork
fi

# Constrói a imagem Docker
docker build --progress=tty -t "${IMAGE_NAME}:${IMAGE_TAG}" .

# Verifica se a construção foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Imagem Docker construída com sucesso: ${IMAGE_NAME}:${IMAGE_TAG}"

    # Executa o contêiner a partir da imagem, usando o IP na rede padrão do Docker
    docker run --net zapnetwork -p "${EXTERNAL_PORT}:8050" --ip 172.22.0."${FOURTH_OCTET}" --privileged -it "${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "Erro ao construir a imagem Docker."
    exit 1
fi

# read -p "Pressione Enter para continuar..."