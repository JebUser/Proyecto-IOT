CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_readings (
    reading_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    sensor_type VARCHAR(20) NOT NULL,
    value VARCHAR(50) NOT NULL,  -- Cambiado a VARCHAR para aceptar cualquier formato
    unit VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO patients (name, gender) VALUES 
('Juan Pérez', 'Male'),
('María García', 'Female'),
('Carlos López', 'Male');