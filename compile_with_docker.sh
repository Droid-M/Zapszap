#!/bin/bash

# docker network create --driver bridge zap_network
pip install 'urllib3<2'
./reset_and_run.sh
docker-compose build
docker-compose run --rm app