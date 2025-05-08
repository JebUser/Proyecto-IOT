CREATE TABLE IF NOT EXISTS lecturas (
    id SERIAL PRIMARY KEY,
    nombre_sensor TEXT NOT NULL,
    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW(),
    tipo_dato TEXT NOT NULL,
    valor NUMERIC(10, 2) NOT NULL
);

