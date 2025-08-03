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

## Configuración de Correo Saliente
Para permitir que el sistema envíe notificaciones por correo (por ejemplo, avisos de préstamos vencidos), es necesario configurar un servidor de correo saliente.
1. Ajustes > Técnico > Correo > Servidores de correo saliente
2. Clic en Nuevo y completar los datos del proveedor de correo, por ejemplo:
| Campo                  | Valor de ejemplo       |
|------------------------|------------------------|
| Nombre                 | `string`               |
| Cifrado de la conexión | `TLS (STARTTLS)`       |
| Servidor SMTP          | `smtp.gmail.com`       |
| Puerto SMTP            | `587`                  |
| Nombre de usuario      | `tucorreo@gmail.com`   |
| Contraseña             | `tu-contraseña`        |

En el caso de la contraseña, se debe de activar las contraseñas de aplicaciones en gmail.

## Parámetros del Sistema

## Verificación Funcional
- Socios de biblioteca
- Gestión de libros
- Préstamos y devoluciones
- Roles y permisos
- Portal web del cliente
- POS para préstamos rápidos
- API REST

### Socios (clientes)
1. Nuevo
2. Rellenar campos solicitados (nombre, apellido, email)
3. Clic en Generar Token Portal
4. El socio recibe un correo para que establezca su contraseña para poder acceder al portal correspondiente
5. Salir

### Libros (productos)
1. Nuevo
2. Rellenar campos solicitados (Nombre del producto, Autor, ISBN, Año de publicación)
3. Seleccionar Tipo de producto > Producto Almacenable
4. Activar "Se puede vender" y "Se puede comprar"
5. Pestaña Ventas clic en "Disponible en PdV" (Punto de venta)
6. Guardar

### Préstamo (POS)
1. Dirigirse al panel de aplicaciones
2. Punto de Venta
3. Seleccionar POS > Nueva Sesión
4. Control de apertura de caja > Abrir sesión
5. Cliente > Seleccionar Cliente
6. Agregar libros al carrito > Pago> Validar > Nueva orden (si así lo desea)
7. Cerrar sesión de POS

### Préstamos
Información relevante de cada préstamo gestionado dentro del sistema POS, incluyendo información de libro, socio, fecha del préstamo, fecha límite, devolución, y estado.
1. Seleccionar préstamo
2. Devolver
3. Enviar Recordatorio en caso de haber sobrepasado la fecha límite de préstamo

## Portal Web Socio
- Acceder a
```bash
http://localhost:8069/
```
- Iniciar Sesión con credenciales enviadas al correo
- Dashboard de Socio (Mis préstamos y Libros disponibles)
- "Mis préstamos" con información sobre su estado, libro solicitado, fecha de préstamo y fecha límite, además de poner renovar (30 días más) o ver el Recibo (Información)
- "Libros disponibles" de solicitar al bibliotecario su préstamo


