#!/bin/bash

# docker network create --driver bridge zap_network
pip install 'urllib3<2'
./remove_files.sh
docker build -t app .
echo "Minha entrada" | docker run --rm --network host -i app