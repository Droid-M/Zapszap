#!/bin/bash

# Verifica se o programa gedit está instalado
if ! command -v gedit &> /dev/null; then
    echo "O programa 'gedit' não está instalado."
    exit 1
fi

# Caminho completo para a pasta logs
log_path="$HOME/Documentos/ZapsShell/src/logs/"

# Verifica se o diretório existe
if [ ! -d "$log_path" ]; then
    echo "O diretório de logs '$log_path' não existe."
    exit 1
fi

# Lista todos os arquivos com a extensão .log no diretório especificado
logs=$(find "$log_path" -type f -name "*.log")

# Abre todos os arquivos .log encontrados no gedit como root, em uma única janela
pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY featherpad $logs
