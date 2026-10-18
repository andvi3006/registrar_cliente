CREATE DATABASE mi_base_de_datos;
use mi_base_de_datos;

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    dni_ruc VARCHAR(15) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
