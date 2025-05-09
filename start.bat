@echo off
echo Iniciando proyecto IoT de salud...
docker-compose down -v
docker-compose build --no-cache
docker-compose up
pause