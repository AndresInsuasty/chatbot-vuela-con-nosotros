-- inicial.sql: crea tablas y datos iniciales para el proyecto chatbot-vuela-con-nosotros

PRAGMA foreign_keys = ON;

-- Tabla de estado de vuelos
CREATE TABLE IF NOT EXISTS estado_vuelos (
    vuelo TEXT PRIMARY KEY,
    estado TEXT NOT NULL,
    origen TEXT NOT NULL,
    destino TEXT NOT NULL,
    fecha TEXT NOT NULL, -- formato YYYY-MM-DD
    hora INTEGER NOT NULL   -- formato HH:MM
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vuelo TEXT NOT NULL,
    id_pasajero TEXT NOT NULL,
    numero_asiento INTEGER NOT NULL,
    FOREIGN KEY(vuelo) REFERENCES estado_vuelos(vuelo) ON DELETE CASCADE
);

-- Inserts de ejemplo para vuelos desde PSO a ASU empezando hoy 2025-10-13
-- Fechas: 2025-10-13, 2025-10-14, 2025-10-15, 2025-10-16, 2025-10-17

INSERT INTO estado_vuelos (vuelo, estado, origen, destino, fecha, hora) VALUES
('PSO-ASU-101','Activo','PSO','ASU','2025-10-13',630),
('PSO-ASU-102','Cancelado','PSO','ASU','2025-10-13',1245),
('PSO-ASU-103','Programado','PSO','ASU','2025-10-14',715),
('PSO-ASU-104','Programado','PSO','ASU','2025-10-14',1800),
('PSO-ASU-105','Programado','PSO','ASU','2025-10-15',900),
('PSO-ASU-106','Programado','PSO','ASU','2025-10-15',1530),
('PSO-ASU-107','Programado','PSO','ASU','2025-10-16',650),
('PSO-ASU-108','Programado','PSO','ASU','2025-10-16',2010),
('PSO-ASU-109','Programado','PSO','ASU','2025-10-17',1100),
('PSO-ASU-110','Programado','PSO','ASU','2025-10-17',1745);

-- Reservas de ejemplo enlazadas a algunos vuelos
-- Reservas de ejemplo: cada vuelo tiene capacidad 10 (asientos 1-10).
-- Aquí dejamos cada vuelo al 50% de ocupación (5 asientos ocupados por vuelo).
INSERT INTO reservas (vuelo, id_pasajero, numero_asiento) VALUES
('PSO-ASU-101','PAX001',1),
('PSO-ASU-101','PAX002',3),
('PSO-ASU-101','PAX003',5),
('PSO-ASU-101','PAX004',7),
('PSO-ASU-101','PAX005',9),

('PSO-ASU-102','PAX006',2),
('PSO-ASU-102','PAX007',4),
('PSO-ASU-102','PAX008',6),
('PSO-ASU-102','PAX009',8),
('PSO-ASU-102','PAX010',10),

('PSO-ASU-103','PAX011',1),
('PSO-ASU-103','PAX012',2),
('PSO-ASU-103','PAX013',3),
('PSO-ASU-103','PAX014',4),
('PSO-ASU-103','PAX015',5),

('PSO-ASU-104','PAX016',6),
('PSO-ASU-104','PAX017',7),
('PSO-ASU-104','PAX018',8),
('PSO-ASU-104','PAX019',9),
('PSO-ASU-104','PAX020',10),

('PSO-ASU-105','PAX021',1),
('PSO-ASU-105','PAX022',3),
('PSO-ASU-105','PAX023',5),
('PSO-ASU-105','PAX024',7),
('PSO-ASU-105','PAX025',9),

('PSO-ASU-106','PAX026',2),
('PSO-ASU-106','PAX027',4),
('PSO-ASU-106','PAX028',6),
('PSO-ASU-106','PAX029',8),
('PSO-ASU-106','PAX030',10),

('PSO-ASU-107','PAX031',1),
('PSO-ASU-107','PAX032',2),
('PSO-ASU-107','PAX033',3),
('PSO-ASU-107','PAX034',4),
('PSO-ASU-107','PAX035',5),

('PSO-ASU-108','PAX036',6),
('PSO-ASU-108','PAX037',7),
('PSO-ASU-108','PAX038',8),
('PSO-ASU-108','PAX039',9),
('PSO-ASU-108','PAX040',10),

('PSO-ASU-109','PAX041',1),
('PSO-ASU-109','PAX042',3),
('PSO-ASU-109','PAX043',5),
('PSO-ASU-109','PAX044',7),
('PSO-ASU-109','PAX045',9),

('PSO-ASU-110','PAX046',2),
('PSO-ASU-110','PAX047',4),
('PSO-ASU-110','PAX048',6),
('PSO-ASU-110','PAX049',8),
('PSO-ASU-110','PAX050',10);
