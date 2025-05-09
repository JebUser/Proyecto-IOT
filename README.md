# Proyecto IoT - Centro de Datos de Salud

Autores:

- Juan Esteban Becerra

- Daniel Vasquez

Sistema de monitoreo de salud con sensores simulados (temperatura, ritmo cardíaco y presión arterial) que envían datos a través de MQTT y se almacenan en PostgreSQL.

## Requisitos

- Docker Desktop
- Docker Compose

## Estructura del sistema

```bash
healthcare-iot/
│
├── docker-compose.yml          # Orquestación de contenedores
├── start.bat                   # Script de inicio (Windows)
├── stop.bat                    # Script de parada (Windows)
│
├── database/
│   ├── init.sql                # Esquema SQL inicial
│   └── Dockerfile              # Configuración personalizada de PostgreSQL
│
├── gateway/                    # IoT Gateway (multi-protocolo)
│   ├── app.py                  # Servidor principal
│   ├── healthcare.proto        # Definición gRPC
│   └── Dockerfile
│
├── subscriber/                 # Subscriptor MQTT-PostgreSQL
│   ├── subscriber.py
│   └── Dockerfile
│
├── sensor-temperature/         # Sensor REST
│   ├── sensor.py
│   └── Dockerfile
│
├── sensor-heartrate/           # Sensor gRPC
│   ├── sensor.py
│   └── Dockerfile
│
└── sensor-bloodpressure/       # Sensor WebSocket
    ├── sensor.py
    └── Dockerfile
```

## Instalación

1. Clonar el repositorio
2. Ejecutar `start.bat` (Windows) o:

   ```bash
   docker-compose up --build
   ```

## Uso y comprobacion en la base de datos

1. Abrir Docker Desktop
2. En la pestaña "Containers", seleccionar el contenedor iot-proyect y buscar postgres
3. Hacer clic en el icono "EXEC" (terminal)
4. Ejecutar:

   ```bash
   psql -U admin healthcare
   ```

### Consultas

```bash
-- Ver todos los pacientes
SELECT * FROM patients;

-- Últimas lecturas
SELECT * FROM sensor_readings ORDER BY timestamp;

--Ultimas 10 lecturas
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;

-- Por metrica
SELECT patient_id, value, unit, timestamp
FROM sensor_readings
WHERE sensor_type = '<<reemplazar tu metrica>>'
ORDER BY timestamp DESC;
```

## Detener el proyecto

Ejecutar Ejecutar `stop.bat` (Windows)

## Comandos útiles

```bash
# Ver tráfico MQTT en tiempo real
docker exec -it mqtt-broker mosquitto_sub -t "healthcare/sensor_data" -v

# Reconstruir solo el gateway
docker-compose build gateway
docker-compose up -d gateway

# Reiniciar solo la base de datos (¡elimina todos los datos!)
docker-compose stop postgres
docker volume rm healthcare-iot_postgres_data
docker-compose up -d postgres
```

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.
