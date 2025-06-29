#!/bin/bash

# Função para confirmar a execução do comando de instalação de dependências
confirmar_execucao() {
    read -p "Deseja executar 'pip install -r requirements.txt'? (s/n): " resposta
    if [[ "$resposta" =~ ^[Ss]$ ]]; then
        pip install -r ~/Documentos/GitHub/Zapszap/src/requirements.txt
    fi
}

confirmar_execucao

sudo python3 ./src/main.py