CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    birth_date DATE NOT NULL,
    document_number VARCHAR(20) NOT NULL UNIQUE,
    phone VARCHAR(20),
    blood_type VARCHAR(5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    sensor_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    protocol VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_readings (
    reading_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    sensor_id INTEGER REFERENCES sensors(sensor_id),
    value VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo para pacientes
INSERT INTO patients (name, gender, birth_date, document_number, phone, blood_type) VALUES 
('Juan Perez', 'Male', '1985-03-15', '12345678', '+57 311 234 5678', 'O+'),
('Maria Garcia', 'Female', '1990-07-22', '87654321', '+57 300 876 5432', 'A+'),
('Carlos Lopez', 'Male', '1978-11-30', '45678912', '+57 315 159 7534', 'B-');

-- Datos para los sensores
INSERT INTO sensors (name, unit, protocol) VALUES
('Temperatura Corporal', '°C', 'REST'),
('Ritmo Cardiaco', 'bpm', 'gRPC'),
('Presion Arterial', 'mmHg', 'WebSocket');