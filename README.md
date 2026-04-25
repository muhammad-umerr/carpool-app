# UniCarpool (Django)

Minimalistic university carpool web app starter with yellow/black UI theme.

## Features implemented

- Public landing page at `/` (login/signup entry)
- User authentication (`login`, `signup`, `logout`)
- Authenticated home page at `/home/` with:
  - available rides listing
  - add-ride form at top
  - multiple pickup stop support per ride
- Current rides status page with:
  - rides you are driving
  - passengers, contacts, pickup locations
  - finalize ride action (driver)
- Payment simulation:
  - available only after driver finalizes ride
  - passenger can simulate payment
- Recent completed rides page:
  - completed as driver
  - completed as passenger

## Tech

- Django 5
- Bootstrap 5 (CDN)
- Custom CSS theme in `static/css/theme.css`

## Quick start (Windows PowerShell)

### 1) Install dependencies

```powershell
Set-Location "c:\Users\umerm\Desktop\carpool-app"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2) Create MySQL database and user

Run these in your MySQL client:

```sql
CREATE DATABASE carpool_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'carpool_user'@'localhost' IDENTIFIED BY 'carpool_password';
GRANT ALL PRIVILEGES ON carpool_db.* TO 'carpool_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3) Set database environment variables

```powershell
$env:MYSQL_DATABASE="carpool_db"
$env:MYSQL_USER="carpool_user"
$env:MYSQL_PASSWORD="carpool_password"
$env:MYSQL_HOST="127.0.0.1"
$env:MYSQL_PORT="3306"
```

### 4) Run migrations and start app

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

### 5) Validate setup

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

If you see `Can't connect to MySQL server on '127.0.0.1'`, start your MySQL service and confirm `MYSQL_HOST` / `MYSQL_PORT` values.

Open `http://127.0.0.1:8000`.

## Phone demo (same Wi-Fi)

Run:

```powershell
Set-Location "c:\Users\umerm\Desktop\carpool-app"
powershell -ExecutionPolicy Bypass -File ".\scripts\run_phone_demo.ps1"
```

The script prints a phone URL like `http://192.168.x.x:8000/`.
If it picks the wrong adapter, set `PHONE_DEMO_IP` to your Wi-Fi IPv4 before running the script.

### Main routes

- `/` -> landing page (public)
- `/accounts/login/` -> login
- `/signup/` -> signup
- `/home/` -> rides home (requires login)
- `/rides/create/` -> add a new ride (requires login)
- `/rides/current/` -> current rides
- `/rides/recent/` -> recent rides

## App structure

- `config/` project settings and root URLs
- `rides/` core app (models, views, routes, tests)
- `templates/` shared and page templates
- `static/css/theme.css` UI theme

## Database

- MySQL is the configured backend in `config/settings.py`.
- PyMySQL is loaded in `config/__init__.py` via `pymysql.install_as_MySQLdb()`.
- Entity relationship diagrams and table notes are in `docs/database-erd.md`.

## Notes for extension

- Keep business logic in service functions later (e.g., matching/fare rules)
- Add university email verification in signup flow
- Add DRF endpoints later if you need mobile or SPA frontend
