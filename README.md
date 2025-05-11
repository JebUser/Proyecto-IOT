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

## Estructura de tópicos MQTT

El sistema utiliza una estructura jerárquica para los tópicos MQTT:

```
data/healthcare/patients/{patient_id}/sensors/{nombre_sensor}
```

Donde:
- `{patient_id}`: El ID del paciente (1, 2, 3, etc.)
- `{nombre_sensor}`: Identificador normalizado del sensor:
  - `body_temperature`: Temperatura corporal
  - `cardiac_rhythm`: Ritmo cardíaco
  - `arterial_pressure`: Presión arterial

Ejemplos:
- Para Juan Pérez (ID=1) y su sensor de temperatura: `data/healthcare/patients/1/sensors/body_temperature`
- Para María García (ID=2) y su sensor de ritmo cardíaco: `data/healthcare/patients/2/sensors/cardiac_rhythm`
- Para Carlos López (ID=3) y su sensor de presión arterial: `data/healthcare/patients/3/sensors/arterial_pressure`

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
docker exec -it postgres psql -U admin healthcare

-- Ver todos los pacientes
SELECT * FROM patients;

-- Ver todos los sensores
SELECT * FROM sensors;

-- Últimas lecturas
SELECT * FROM sensor_readings ORDER BY timestamp;

--Ultimas 10 lecturas
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;

-- Por metrica
SELECT
    p.name AS nombre_paciente,
    s.name AS nombre_sensor,
    sr.value AS valor,
    s.unit AS unidad,
    sr.timestamp AS tiempo
FROM
    sensor_readings sr
JOIN
    patients p ON sr.patient_id = p.patient_id
JOIN
    sensors s ON sr.sensor_id = s.sensor_id
WHERE
    s.sensor_id = <<reemplazar>>
ORDER BY
    sr.timestamp DESC;
```

## Detener el proyecto

Ejecutar Ejecutar `stop.bat` (Windows)

## Comandos útiles

```bash
# Ver tráfico MQTT en tiempo real (usar test-mqtt-topics.bat)
docker exec -it mqtt-broker mosquitto_sub -t "data/healthcare/patients/+/sensors/+" -v

# Escuchar un sensor específico para un paciente
docker exec -it mqtt-broker mosquitto_sub -t "data/healthcare/patients/1/sensors/body_temperature" -v

# Publicar un mensaje de prueba manualmente
docker exec -it mqtt-broker mosquitto_pub -t "data/healthcare/patients/1/sensors/body_temperature" -m '{"value": "37.2"}'

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
