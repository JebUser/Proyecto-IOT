#!/bin/bash

echo "Deteniendo contenedores..."
docker-compose down -v --remove-orphans

echo "Proyecto detenido y volumenes eliminados."
