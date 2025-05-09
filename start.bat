#!/bin/bash

echo "Construyendo contenedores..."
docker-compose build

echo "Levantando proyecto..."
docker-compose up -d

echo "Proyecto iniciado. Usa 'docker-compose logs -f' para ver logs."
