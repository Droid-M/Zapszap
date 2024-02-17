#!/bin/bash

# Caminhos completos para as pastas logs e backups
log_path="$HOME/Documentos/GitHub/Zapszap/src/logs/"
backup_path="$HOME/Documentos/GitHub/Zapszap/src/backups/"

# Função para remover arquivos .log e .zap que não começam com underscore
remove_logs_and_zaps() {
    local path=$1
    sudo find "$path" -type f \( -name "*.log" -o -name "*.zap" \) ! -name "_*.log" ! -name "_*.zap" -exec sudo rm {} \;
}

# Verifica se os diretórios existem
if [ ! -d "$log_path" ]; then
    echo "O diretório de logs '$log_path' não existe."
    exit 1
fi

if [ ! -d "$backup_path" ]; then
    echo "O diretório de backups '$backup_path' não existe."
    exit 1
fi

# Remove arquivos .log e .zap das pastas logs e backups
remove_logs_and_zaps "$log_path"
remove_logs_and_zaps "$backup_path"

echo "Arquivos .log e .zap removidos, exceto aqueles que começam com underscore."
