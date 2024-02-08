#!/bin/bash

# Verifica se o número de argumentos é suficiente
if [ "$#" -lt 4 ]; then
    echo "Uso: $0 <NOME_IMAGEM> <TAG_IMAGEM> <QUARTO_OCTETO> <PORTA_EXTERNA>"
    exit 1
fi

# Nome, tag da imagem Docker
IMAGE_NAME="$1"
IMAGE_TAG="$2"
FOURTH_OCTET="$3"
EXTERNAL_PORT="$4"

# Caminho do diretório no host
HOST_DIRECTORY="/home/marcos/Área de Trabalho/zap2"

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

    # Cria um volume para persistir dados entre reinicializações
    VOLUME_NAME="zap_data_${FOURTH_OCTET}"
    docker volume create "${VOLUME_NAME}"

    # Executa o contêiner a partir da imagem, usando o IP na rede padrão do Docker e monta o volume
    docker run --name zap_container_"${FOURTH_OCTET}" --net zapnetwork -p "${EXTERNAL_PORT}:8050" --ip 172.22.0."${FOURTH_OCTET}" --privileged -v "${HOST_DIRECTORY}:/app/data" -it "${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "Erro ao construir a imagem Docker."
    exit 1
fi

# read -p "Pressione Enter para continuar..."

###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################

# #!/bin/bash

# # Verifica se o número de argumentos é suficiente
# if [ "$#" -lt 4 ]; then
#     echo "Uso: $0 <NOME_IMAGEM> <TAG_IMAGEM> <QUARTO_OCTETO> <PORTA_EXTERNA>"
#     exit 1
# fi

# # Nome, tag da imagem Docker
# IMAGE_NAME="$1"
# IMAGE_TAG="$2"
# FOURTH_OCTET="$3"
# EXTERNAL_PORT="$4"

# # Verifica se o Docker está instalado
# if ! command -v docker &> /dev/null; then
#     echo "Docker não está instalado. Por favor, instale o Docker para continuar."
#     exit 1
# fi

# # Verifica se a rede já existe
# if ! docker network inspect zapnetwork &> /dev/null; then
#     # Cria uma rede bridge personalizada com um IP específico
#     docker network create --subnet=172.22.0.0/16 zapnetwork
# fi

# # Tenta iniciar o container existente
# docker start -a zap_container_"${FOURTH_OCTET}"

# # Se o container não estiver em execução, cria um novo
# if [ $? -ne 0 ]; then
#     # Constrói a imagem Docker
#     docker build --progress=tty -t "${IMAGE_NAME}:${IMAGE_TAG}" .

#     # Verifica se a construção foi bem-sucedida
#     if [ $? -eq 0 ]; then
#         echo "Imagem Docker construída com sucesso: ${IMAGE_NAME}:${IMAGE_TAG}"

#         # Cria um volume para persistir dados entre reinicializações
#         VOLUME_NAME="zap_data_${FOURTH_OCTET}"
#         docker volume create "${VOLUME_NAME}"

#         # Executa o contêiner a partir da imagem, usando o IP na rede padrão do Docker e monta o volume
#         docker run --name zap_container_"${FOURTH_OCTET}" --net zapnetwork -p "${EXTERNAL_PORT}:8050" --ip 172.22.0."${FOURTH_OCTET}" --privileged -v "${VOLUME_NAME}:/app/data" -it "${IMAGE_NAME}:${IMAGE_TAG}"
#     else
#         echo "Erro ao construir a imagem Docker."
#         exit 1
#     fi
# fi
