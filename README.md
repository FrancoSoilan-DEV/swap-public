<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=120&color=gradient&reversal=true&text=Django%20SWAP&fontColor=ffffff&fontSize=40&fontAlignY=35&desc=Internal%20Management%20System%20%7C%20Docker%20%7C%20PostgreSQL&descAlignY=55&descSize=18" />
</div>

<div align="center">

# Django SWAP

**Docker-ready Django internal management system for business operations, role-based modules, inventory, backups, gatehouse records, technical service, Excel exports, and PDF reports.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-ready-499848?style=for-the-badge)](https://gunicorn.org)

</div>

---

> [!IMPORTANT]
> ## First command you should remember
>
> After starting the Docker containers:
>
> ```bash
> docker compose up --build
> ```
>
> Run this command:
>
> ```bash
> docker compose exec web sh scripts/docker-init.sh
> ```
>
> This is the most important setup command for the project.
>
> It runs:
>
> ```bash
> python manage.py migrate --noinput
> python manage.py seed_initial_data
> python manage.py collectstatic --noinput
> ```
>
> Without this step, the project may start, but many modules will not work correctly because the system depends on initial users, groups, statuses, departments, backup days, maintenance states, equipment types, and default values.

---

# English

## About Django SWAP

**Django SWAP** is a Django-based internal management system designed to organize and control several operational areas of a company.

This public version is prepared to run locally with Docker without affecting the production repository or production database.

The system includes modules for:

- User authentication.
- Role-based access.
- Human Resources / TTHH.
- IT / Informatica.
- Gatehouse / Porteria.
- Technician panel / Tecnico.
- Technical Service / Servicio Tecnico.
- Weekly backup control.
- Backup history.
- Inventory management.
- Equipment management.
- Maintenance calendar.
- Entry and exit records.
- Technical work registration.
- Excel exports.
- PDF exports.

---

## Public repository

- Repository: https://github.com/FrancoSoilan-DEV/Django-swap
- Clone URL:

```bash
git clone https://github.com/FrancoSoilan-DEV/Django-swap.git
```

---

## Important setup command

After running Docker, always initialize the project with:

```bash
docker compose exec web sh scripts/docker-init.sh
```

This command must be executed after:

```bash
docker compose up --build
```

The initialization script applies migrations, loads required base data, and collects static files.

---

## Main technologies

- Python 3.12
- Django 5
- PostgreSQL 15
- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Redis
- OpenPyXL
- ReportLab
- python-decouple
- dj-database-url

---

## Project structure

```text
Django-swap/
│
├── swap/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── swap_home/
├── swap_tthh/
├── swap_informatica/
├── swap_porteria/
├── swap_tecnico/
├── swap_serviciotecnico/
│
├── templates/
├── static/
├── scripts/
│   └── docker-init.sh
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
└── README.md
```

---

## Apps overview

### `swap_home`

Main authentication app.

Responsibilities:

- Login view.
- Logout view.
- User authentication.
- Redirect users based on their Django group.

Main groups:

```text
TTHH
Informatica
Porteria
Tecnico
ServicioTecnico
```

---

### `swap_tthh`

Human Resources module.

Responsibilities:

- Employees / funcionarios.
- Departments.
- Internal phone numbers.
- Employee entry history.
- Provider records.
- Collector records.
- Visitor records.
- General tasks.
- TTHH tasks.
- Excel exports.
- PDF exports.

---

### `swap_informatica`

IT module.

Responsibilities:

- Weekly backups.
- Backup states.
- Backup history.
- Backup assignments.
- Employees with equipment.
- Inventory.
- Equipment records.
- Equipment types.
- Maintenance calendar.
- Maintenance states.
- Maintenance history.
- Excel exports.

Important business logic:

- Backups are grouped by week.
- Weekly reset logic uses a stored week control.
- Backups can be marked as completed once per week.
- The system depends on backup states like:
  - `Pendiente⏳`
  - `Finalizado✅`
  - `Inactivo❌`

---

### `swap_porteria`

Gatehouse / access control module.

Responsibilities:

- Employee entries.
- Provider entries.
- Collector entries.
- Visitor entries.
- Entry status management.
- Exit registration.
- Entry history.

Important business logic:

- New entries usually start with the state:
  - `Pendiente⚠️`
- Completed entries use:
  - `Finalizado✅`

---

### `swap_tecnico`

Technician module.

Responsibilities:

- Allows technicians to register completed technical work.
- Shows the logged-in technician's own records.
- Uses the logged-in user's first and last name to associate records.
- Restricts access based on the `Tecnico` group.
- Includes a date-based access rule.

Important business logic:

- New technical jobs start with:
  - `Pendiente⚠️`
- New technical jobs use default amount:
  - `0`

---

### `swap_serviciotecnico`

Technical Service administration module.

Responsibilities:

- Review technical jobs.
- Edit states and amounts.
- Bulk update technical records.
- View historical technical work.
- Generate Excel reports.
- Analyze work records by date, month, year, technician, and state.

---

## Environment variables

Create a `.env` file in the project root.

Example:

```env
DEBUG=True
SECRET_KEY=clave-local
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

POSTGRES_DB=swap_public
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

DATABASE_URL=postgres://postgres:admin@db:5432/swap_public

DJANGO_ADMIN_PASSWORD=admin123
DJANGO_TTHH_PASSWORD=tthh123
DJANGO_INFORMATICA_PASSWORD=informatica123
DJANGO_PORTERIA_PASSWORD=porteria123
DJANGO_TECNICO_PASSWORD=tecnico123
DJANGO_SERVICIO_TECNICO_PASSWORD=servicio123
```

> [!WARNING]
> Do not commit your real `.env` file to a public repository.
>
> Use `.env.example` to document the required variables.

---

## Recommended `.env.example`

You can include this file safely in the public repository:

```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

POSTGRES_DB=swap_public
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

DATABASE_URL=postgres://postgres:admin@db:5432/swap_public

DJANGO_ADMIN_PASSWORD=admin123
DJANGO_TTHH_PASSWORD=tthh123
DJANGO_INFORMATICA_PASSWORD=informatica123
DJANGO_PORTERIA_PASSWORD=porteria123
DJANGO_TECNICO_PASSWORD=tecnico123
DJANGO_SERVICIO_TECNICO_PASSWORD=servicio123
```

---

## Recommended `.gitignore`

Make sure your `.gitignore` includes:

```gitignore
.env
data/
staticfiles/
media/
*.sqlite3
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv/
.idea/
.vscode/
```

The `data/` directory is used by Docker volumes for local PostgreSQL and Redis data.

---

## Running the project with Docker

### 1. Clone the repository

```bash
git clone https://github.com/FrancoSoilan-DEV/Django-swap.git
cd Django-swap
```

### 2. Create the `.env` file

Create a `.env` file in the project root using the example shown above.

### 3. Build and start the containers

```bash
docker compose up --build
```

### 4. Initialize the system

In another terminal, run:

```bash
docker compose exec web sh scripts/docker-init.sh
```

### 5. Open the project

```text
http://localhost:8000
```

---

## Default users created by the initialization script

The command:

```bash
docker compose exec web sh scripts/docker-init.sh
```

loads the initial users through the Django command:

```bash
python manage.py seed_initial_data
```

Default access credentials:

| Role | Username | Password | Destination |
|---|---|---|---|
| Admin | `admin` | `admin123` | Django Admin |
| Human Resources | `tthh` | `tthh123` | TTHH module |
| IT | `informatica` | `informatica123` | Informatica module |
| Gatehouse | `porteria` | `porteria123` | Porteria module |
| Technician | `tecnico` | `tecnico123` | Tecnico module |
| Technical Service | `serviciotecnico` | `servicio123` | Servicio Tecnico module |

If you change the password variables in `.env`, the seed command will use those values when creating users for the first time.

> [!NOTE]
> The seed command is idempotent. It can be executed more than once without duplicating the base records.

---

## Initial data loaded by `seed_initial_data`

The command creates the minimum required data for the system to work correctly.

It creates:

- Django groups.
- Default users.
- Departments.
- Task days.
- Task states.
- Entry states.
- Backup days.
- Backup states.
- Backup week control.
- Disks.
- Inventory deposits.
- Inventory categories.
- Inventory states.
- Equipment types.
- Maintenance types.
- Maintenance states.
- Technical service amounts.
- Demo employee.
- Demo collector.
- Demo provider.

Some important values created by the seed command:

```text
TTHH
Informatica
Porteria
Tecnico
ServicioTecnico

General
Pendiente⚠️
Finalizado✅
Cancelar❌

Pendiente⏳
Inactivo❌

PC
Notebook
UPS
Impresora
Router
DVR
Laser
Scaner
Rack
Switch
Servidor
Monitor
```

These values are important because several views search records by exact names.

---

## Docker services

The `docker-compose.yml` file defines three services:

### `web`

Runs the Django application using Gunicorn.

### `db`

Runs PostgreSQL 15.

### `redis`

Runs Redis 7.

---

## Database connection inside Docker

Inside Docker, the database host must be:

```text
db
```

That is why the `DATABASE_URL` should be:

```env
DATABASE_URL=postgres://postgres:admin@db:5432/swap_public
```

Do not use `localhost` as the database host inside Docker.

Inside the `web` container, `localhost` means the Django container itself, not the PostgreSQL container.

---

## Useful Docker commands

Start the project:

```bash
docker compose up --build
```

Start in detached mode:

```bash
docker compose up --build -d
```

Stop containers:

```bash
docker compose down
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Run the seed command:

```bash
docker compose exec web python manage.py seed_initial_data
```

Collect static files:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

Open Django shell:

```bash
docker compose exec web python manage.py shell
```

Create a superuser manually:

```bash
docker compose exec web python manage.py createsuperuser
```

Run the full initialization script:

```bash
docker compose exec web sh scripts/docker-init.sh
```

---

## Resetting the local database

If you need a clean local database, stop the containers:

```bash
docker compose down
```

Then delete the local Docker data folder.

On Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .\data
```

On Linux / macOS:

```bash
rm -rf ./data
```

Then start again:

```bash
docker compose up --build
```

And initialize again:

```bash
docker compose exec web sh scripts/docker-init.sh
```

---

## Static files

Static files are handled with WhiteNoise.

They are collected with:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

The initialization script already runs this command.

---

## Production safety

This public version should stay separated from the production project.

To avoid affecting production:

- Do not use the production `.env`.
- Do not use the production `DATABASE_URL`.
- Do not connect this repository to the production deployment.
- Do not push this code to the production repository.
- Do not share production secrets.
- Do not commit real credentials.
- Do not commit local database data.
- Keep this project connected only to its own public repository.

---

## Common issues

### `Unknown command: seed_initial_data`

Check that the command file exists at:

```text
swap_home/management/commands/seed_initial_data.py
```

Also make sure these files exist:

```text
swap_home/management/__init__.py
swap_home/management/commands/__init__.py
```

---

### `.env unexpected character "/"`

This happens when the `.env` file contains invalid lines like:

```text
admin / admin123
```

`.env` files only accept this format:

```env
VARIABLE=value
```

Use a `README.md` or documentation file to show login credentials, not raw text inside `.env`.

---

### Database connection error

Make sure `DATABASE_URL` uses `db` as host:

```env
DATABASE_URL=postgres://postgres:admin@db:5432/swap_public
```

Do not use:

```env
DATABASE_URL=postgres://postgres:admin@localhost:5432/swap_public
```

---

### Data already exists

That is normal. The seed command uses `get_or_create`, so it will not duplicate most base records.

---

# Español

## Acerca de Django SWAP

**Django SWAP** es un sistema interno de gestión desarrollado con Django. Está diseñado para organizar y controlar distintas áreas operativas de una empresa.

Esta versión pública está preparada para correr localmente con Docker sin afectar el repositorio de producción ni la base de datos real de producción.

El sistema incluye módulos para:

- Autenticación de usuarios.
- Acceso según roles.
- Talento Humano / TTHH.
- Informática.
- Portería.
- Técnicos.
- Servicio Técnico.
- Control de backups semanales.
- Historial de backups.
- Inventario.
- Gestión de equipos.
- Calendario de mantenimientos.
- Registros de entrada y salida.
- Carga de trabajos técnicos.
- Exportaciones a Excel.
- Exportaciones a PDF.

---

## Comando más importante

Después de levantar Docker:

```bash
docker compose up --build
```

Inicializa el proyecto con:

```bash
docker compose exec web sh scripts/docker-init.sh
```

El script de inicialización aplica migraciones, carga datos iniciales obligatorios y recolecta archivos estáticos.

---

## Tecnologías principales

- Python 3.12
- Django 5
- PostgreSQL 15
- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Redis
- OpenPyXL
- ReportLab
- python-decouple
- dj-database-url

---

## Estructura del proyecto

```text
Django-swap/
│
├── swap/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── swap_home/
├── swap_tthh/
├── swap_informatica/
├── swap_porteria/
├── swap_tecnico/
├── swap_serviciotecnico/
│
├── templates/
├── static/
├── scripts/
│   └── docker-init.sh
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
└── README.md
```

---

## Resumen de apps

### `swap_home`

App principal de autenticación.

Responsabilidades:

- Login.
- Logout.
- Autenticación.
- Redirección según el grupo del usuario.

Grupos principales:

```text
TTHH
Informatica
Porteria
Tecnico
ServicioTecnico
```

---

### `swap_tthh`

Módulo de Talento Humano.

Responsabilidades:

- Funcionarios.
- Departamentos.
- Teléfonos internos.
- Historial de entradas de funcionarios.
- Registros de proveedores.
- Registros de cobradores.
- Registros de visitas.
- Tareas generales.
- Tareas de TTHH.
- Exportaciones a Excel.
- Exportaciones a PDF.

---

### `swap_informatica`

Módulo de Informática.

Responsabilidades:

- Backups semanales.
- Estados de backups.
- Historial de backups.
- Asignación de backups.
- Funcionarios con equipos.
- Inventario.
- Equipos.
- Tipos de equipos.
- Calendario de mantenimiento.
- Estados de mantenimiento.
- Historial de mantenimiento.
- Exportaciones a Excel.

Lógica importante:

- Los backups se agrupan por semana.
- El reset semanal usa un control persistente.
- Un backup puede guardarse como realizado una vez por semana.
- El sistema depende de estados como:
  - `Pendiente⏳`
  - `Finalizado✅`
  - `Inactivo❌`

---

### `swap_porteria`

Módulo de Portería y control de acceso.

Responsabilidades:

- Entrada de funcionarios.
- Entrada de proveedores.
- Entrada de cobradores.
- Entrada de visitas.
- Gestión de estados de entrada.
- Registro de salidas.
- Historial de entradas.

Lógica importante:

- Las nuevas entradas normalmente empiezan con:
  - `Pendiente⚠️`
- Las entradas completadas usan:
  - `Finalizado✅`

---

### `swap_tecnico`

Módulo para técnicos.

Responsabilidades:

- Permite que los técnicos carguen trabajos realizados.
- Muestra los registros del técnico logueado.
- Usa el nombre y apellido del usuario logueado para relacionar trabajos.
- Restringe acceso según el grupo `Tecnico`.
- Incluye una regla de acceso basada en fechas.

Lógica importante:

- Los nuevos trabajos técnicos empiezan con:
  - `Pendiente⚠️`
- Los nuevos trabajos técnicos usan monto por defecto:
  - `0`

---

### `swap_serviciotecnico`

Módulo de administración de Servicio Técnico.

Responsabilidades:

- Revisión de trabajos técnicos.
- Edición de estados y montos.
- Edición masiva de registros.
- Historial de trabajos técnicos.
- Reportes en Excel.
- Análisis por fecha, mes, año, técnico y estado.

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
DEBUG=True
SECRET_KEY=clave-local
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

POSTGRES_DB=swap_public
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

DATABASE_URL=postgres://postgres:admin@db:5432/swap_public

DJANGO_ADMIN_PASSWORD=admin123
DJANGO_TTHH_PASSWORD=tthh123
DJANGO_INFORMATICA_PASSWORD=informatica123
DJANGO_PORTERIA_PASSWORD=porteria123
DJANGO_TECNICO_PASSWORD=tecnico123
DJANGO_SERVICIO_TECNICO_PASSWORD=servicio123
```

> [!WARNING]
> No subas tu `.env` real a un repositorio público.
>
> Usa `.env.example` para documentar las variables necesarias.

---

## Ejecutar el proyecto con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/FrancoSoilan-DEV/Django-swap.git
cd Django-swap
```

### 2. Crear el archivo `.env`

Crea un archivo `.env` en la raíz usando el ejemplo anterior.

### 3. Construir y levantar contenedores

```bash
docker compose up --build
```

### 4. Inicializar el sistema

En otra terminal:

```bash
docker compose exec web sh scripts/docker-init.sh
```

### 5. Abrir el proyecto

```text
http://localhost:8000
```

---

## Usuarios iniciales creados por el script

El comando:

```bash
docker compose exec web sh scripts/docker-init.sh
```

carga los usuarios iniciales mediante:

```bash
python manage.py seed_initial_data
```

Credenciales por defecto:

| Rol | Usuario | Contraseña | Destino |
|---|---|---|---|
| Admin | `admin` | `admin123` | Panel de Django Admin |
| Talento Humano | `tthh` | `tthh123` | Módulo TTHH |
| Informática | `informatica` | `informatica123` | Módulo Informática |
| Portería | `porteria` | `porteria123` | Módulo Portería |
| Técnico | `tecnico` | `tecnico123` | Módulo Técnico |
| Servicio Técnico | `serviciotecnico` | `servicio123` | Módulo Servicio Técnico |

Si cambias las variables de contraseña en `.env`, el comando seed usará esos valores al crear los usuarios por primera vez.

> [!NOTE]
> El comando seed es idempotente. Puedes ejecutarlo más de una vez sin duplicar la mayoría de los datos base.

---

## Datos iniciales cargados por `seed_initial_data`

El comando crea los datos mínimos necesarios para que el sistema funcione correctamente.

Crea:

- Grupos de Django.
- Usuarios por defecto.
- Departamentos.
- Días de tareas.
- Estados de tareas.
- Estados de entrada.
- Días de backup.
- Estados de backup.
- Control semanal de backups.
- Discos.
- Depósitos de inventario.
- Categorías de inventario.
- Estados de inventario.
- Tipos de equipo.
- Tipos de mantenimiento.
- Estados de mantenimiento.
- Montos de Servicio Técnico.
- Funcionario demo.
- Cobrador demo.
- Proveedor demo.

Algunos valores importantes creados por el seed:

```text
TTHH
Informatica
Porteria
Tecnico
ServicioTecnico

General
Pendiente⚠️
Finalizado✅
Cancelar❌

Pendiente⏳
Inactivo❌

PC
Notebook
UPS
Impresora
Router
DVR
Laser
Scaner
Rack
Switch
Servidor
Monitor
```

Estos valores son importantes porque varias vistas buscan registros por nombres exactos.

---

## Servicios Docker

El archivo `docker-compose.yml` define tres servicios:

### `web`

Ejecuta la aplicación Django con Gunicorn.

### `db`

Ejecuta PostgreSQL 15.

### `redis`

Ejecuta Redis 7.

---

## Conexión a la base de datos dentro de Docker

Dentro de Docker, el host de la base de datos debe ser:

```text
db
```

Por eso el `DATABASE_URL` debe ser:

```env
DATABASE_URL=postgres://postgres:admin@db:5432/swap_public
```

No uses `localhost` como host de la base de datos dentro de Docker.

Dentro del contenedor `web`, `localhost` significa el propio contenedor de Django, no el contenedor de PostgreSQL.

---

## Comandos útiles de Docker

Levantar el proyecto:

```bash
docker compose up --build
```

Levantar en segundo plano:

```bash
docker compose up --build -d
```

Detener contenedores:

```bash
docker compose down
```

Ejecutar migraciones:

```bash
docker compose exec web python manage.py migrate
```

Ejecutar seed:

```bash
docker compose exec web python manage.py seed_initial_data
```

Recolectar estáticos:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

Abrir shell de Django:

```bash
docker compose exec web python manage.py shell
```

Crear superusuario manualmente:

```bash
docker compose exec web python manage.py createsuperuser
```

Ejecutar inicialización completa:

```bash
docker compose exec web sh scripts/docker-init.sh
```

---

## Resetear la base de datos local

Si necesitas una base local limpia, detén los contenedores:

```bash
docker compose down
```

Luego borra la carpeta local de datos.

En Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .\data
```

En Linux / macOS:

```bash
rm -rf ./data
```

Después vuelve a levantar:

```bash
docker compose up --build
```

E inicializa otra vez:

```bash
docker compose exec web sh scripts/docker-init.sh
```

---

## Archivos estáticos

Los archivos estáticos se manejan con WhiteNoise.

Se recolectan con:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

El script de inicialización ya ejecuta este comando.

---

## Seguridad para no afectar producción

Esta versión pública debe mantenerse separada del proyecto de producción.

Para evitar afectar producción:

- No uses el `.env` de producción.
- No uses el `DATABASE_URL` de producción.
- No conectes este repositorio al deploy de producción.
- No hagas push de este código al repositorio de producción.
- No compartas secretos reales.
- No subas credenciales reales.
- No subas datos locales de la base de datos.
- Mantén este proyecto conectado únicamente a su propio repositorio público.

---

## Problemas comunes

### `Unknown command: seed_initial_data`

Verifica que el archivo exista en:

```text
swap_home/management/commands/seed_initial_data.py
```

También verifica que existan:

```text
swap_home/management/__init__.py
swap_home/management/commands/__init__.py
```

---

### `.env unexpected character "/"`

Esto pasa cuando el `.env` contiene líneas inválidas como:

```text
admin / admin123
```

Los archivos `.env` solo aceptan este formato:

```env
VARIABLE=valor
```

Las credenciales visibles deben documentarse en el `README.md`, no como texto suelto dentro del `.env`.

---

### Error de conexión a la base de datos

Asegúrate de que `DATABASE_URL` use `db` como host:

```env
DATABASE_URL=postgres://postgres:admin@db:5432/swap_public
```

No uses:

```env
DATABASE_URL=postgres://postgres:admin@localhost:5432/swap_public
```

---

### Los datos ya existen

Eso es normal. El comando seed usa `get_or_create`, por lo que no debería duplicar la mayoría de los registros base.

---

## Final note

This project is a public, Docker-ready version of Django SWAP. It is intended for local testing, demonstration, learning, and further development without touching the production environment.

---

## Nota final

Este proyecto es una versión pública de Django SWAP preparada para Docker. Está pensada para pruebas locales, demostración, aprendizaje y desarrollo sin tocar el entorno de producción.

---

<div align="center">
  <h3>Built with Django, PostgreSQL, Docker, Redis, and real operational workflows.</h3>
</div>

<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=gradient&section=footer" />
</div>
