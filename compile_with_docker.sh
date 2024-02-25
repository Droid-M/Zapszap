#!/bin/bash

# docker network create --driver bridge zap_network
pip install 'urllib3<2'
./remove_files.sh
docker-compose build
docker-compose run --rm app