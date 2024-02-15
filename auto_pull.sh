#!/bin/bash

# Loop infinito
while :
do
    # Executa o comando git pull para atualizar o repositório
    git pull

    # Executa o comando git merge para mesclar quaisquer alterações remotas
    git merge

    # Aguarda 1 minuto antes de repetir o loop
    sleep 5
done