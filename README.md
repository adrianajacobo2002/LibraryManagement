# Library Management Module - Odoo 17

Sistema de gestión de biblioteca desarrollado como parte de una prueba técnica para Odoo Developer. Este proyecto incluye funcionalidades como gestión de socios, préstamos, renovaciones, acceso por portal y servicios API REST para disponibilidad de libros.

## Requisitos Previos
Docker y Docker Compose instalados
Puerto 8069 disponible

## Instalación General
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
   Llenando los campos solicitados

6. Iniciar Sesión
   Con las credenciales creadas con anterioridad

## Instalación del Módulo Library Management
El módulo debe estar dentro de la carpeta addons/ incluída en este repositorio

1. Activar el modo desarrollador en Odoo
   - Dentro de http://localhost:8069/web
   - Hacer clic en el panel de aplicaciones
   - Ajustes
   - "Activar el modo desarrollador"
2. Actualizar lista de aplicaciones
   - En el menú de Apps
   - Clic en "Actualizar lista de aplicaciones"
   - Buscar Library Management
   - Clic en "Instalar"
3. Asignar Rol de Bibliotecario
   - Ajusted > Usuarios > Administrar usuarios
   - Seleccionar el usuario Administrator
   - En la pestaña OTHER, localizar la sección Library
   - Cambiar el rol A Bibliotecario
   - Guardar los cambios
4. Acceder a Biblioteca por medio del panel de aplicaciones
  
## Verificación Funcional
- Gestión de libros
- Socios de biblioteca
- Préstamos y devoluciones
- Roles y permisos
- Portal web del cliente
- POS para préstamos rápidos
- API REST

##Socios (clientes)
1. Nuevo
2. Rellenar campos solicitados (nombre, apellido, email)
3. Clic en Generar Token Portal
4. Salir

## Libros (productos)


