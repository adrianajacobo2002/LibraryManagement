# Library Management Module - Odoo 17

Sistema de gestión de biblioteca desarrollado como parte de una prueba técnica para Odoo Developer. Este proyecto incluye funcionalidades como gestión de socios, préstamos, renovaciones, acceso por portal y servicios API REST para disponibilidad de libros.

## Requisitos Previos
Docker y Docker Compose instalados
Puerto 8069 disponible

## Instalación
1. Clonar este repositorio
```bash
git clone https://github.com/adrianajacobo2002/LibraryManagement.git
```
```bash
cd library_management
```
2. Iniciar los servicios con Docker Compose
```bash
docker-compose up --build
```
Esto ejecutará los siguientes servicios:
- web: Odoo 17 en el puerto 8069.
- db: PostgreSQL 15 en el puerto 5433.

3. Acceder a Odoo
En el navegador abrir:
```bash
http://localhost:8069/web
```
4. Crear una nueva base de datos
Estructura del Proyecto
Requerimientos
Odoo: [17]
Python
Docker y Docker Compose
Cuenta de correo Gmail (para configuración SMTP) 
Git

Instalación y configuración
Clonar el repositorio
git clone [text](https://github.com/adrianajacobo2002/LibraryManagement.git)


Levantar el entorno usando Docker
docker compose up -d

Esto levantará:
Contenedor de Odoo en el puerto 8069
Contenedor de PostgreSQL como base de datos

