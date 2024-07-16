DROP TABLE IF EXISTS ets;
CREATE TABLE ets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vivienda TEXT NOT NULL,
    codigopartida TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    detalle TEXT NOT NULL,
    caracteristicas TEXT NOT NULL
);