CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    protocolo TEXT NOT NULL
);

CREATE TABLE lecturas (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensores(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    valor NUMERIC(10, 2) NOT NULL
);
