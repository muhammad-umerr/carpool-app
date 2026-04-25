# Django vs MySQL: Roles and Relationship

## TL;DR
- **MySQL** = persistent storage layer (database server).
- **Django** = application framework that abstracts database interactions via an ORM.
- They work together: Django **models** map to MySQL **tables**; Django **querysets** become MySQL **SQL queries**.

---

## Detailed Breakdown

### MySQL's Role
MySQL is a **relational database management system (RDBMS)**:
- Stores tables with rows and columns.
- Enforces constraints (foreign keys, unique indexes, data types).
- Executes SQL queries and returns results.
- Manages transactions, concurrency, and persistence.
- Does NOT know about your application logic—only about SQL.

**In this project:** MySQL stores all ride, participant, and user data. It runs on `localhost:3306` (or wherever `MYSQL_HOST` points).

### Django's Role
Django is a **Python web framework** with an ORM (Object-Relational Mapper):
- Provides a Python API to query/insert/update/delete data instead of writing raw SQL.
- Models (like `Ride`, `RideParticipant`) represent database tables in Python.
- Handles migrations (schema versioning).
- Provides views, forms, authentication, and templating.
- Translates Python code into SQL behind the scenes.

**In this project:** Django receives HTTP requests, queries MySQL via the ORM, and returns HTML responses.

---

## How They Connect

### 1. Model Definition (Django)
```python
class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=120)
    departure_time = models.DateTimeField()
```

### 2. Migration (Django ? MySQL)
Django's `manage.py migrate` command:
- Reads model definitions.
- Generates SQL (CREATE TABLE, ADD COLUMN, etc.).
- Executes SQL on MySQL.
- Records migration history in `django_migrations` table.

### 3. Query (Django ? MySQL ? Django)
```python
# Django ORM query (Python)
rides = Ride.objects.filter(status='OPEN').order_by('departure_time')

# Becomes (SQL)
SELECT * FROM rides_ride WHERE status = 'OPEN' ORDER BY departure_time;

# MySQL executes and returns rows
# Django converts rows back to Python Ride objects
```

### 4. Data Persistence (MySQL)
- Django commits changes to MySQL via transactions.
- MySQL persists data to disk.
- Data survives server restarts.

---

## Why Use Django Instead of Raw MySQL?

| Feature | Raw MySQL | Django ORM |
|---------|-----------|-----------|
| Security (SQL injection) | Vulnerable | Protected (parameterized queries) |
| Data Validation | Manual | Built-in (model fields) |
| Schema Versioning | Manual `ALTER TABLE` | Automatic migrations |
| Code Reusability | Ad-hoc SQL strings | Reusable model queryset methods |
| Type Safety | None | Python type hints |
| Foreign Key Handling | Manual JOINs | Automatic relationships |

---

## Key Takeaway
**Django is NOT a database.** It's a framework that **uses** MySQL as a database. You could swap MySQL for PostgreSQL, SQLite, or Oracle—Django abstracts that away. The business logic stays in Django; the data stays in MySQL.

---

## Configuration in This Project

### settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Use MySQL driver
        'NAME': os.getenv('MYSQL_DATABASE', 'carpool_db'),
        'USER': os.getenv('MYSQL_USER', 'carpool_user'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'carpool_password'),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
    }
}
```

This tells Django:
- Which database backend to use (`mysql`).
- Where MySQL server is running (`HOST` + `PORT`).
- Which database, username, and password to connect with.

### __init__.py
```python
import pymysql
pymysql.install_as_MySQLdb()
```

This tells Django to use **PyMySQL** (a pure-Python MySQL driver) instead of the legacy MySQLdb library.

---

## Common Commands

### See the actual SQL Django generates
```bash
python manage.py sqlmigrate rides 0001
```

### Create tables in MySQL (first time)
```bash
python manage.py migrate
```

### Query directly (debug)
```bash
python manage.py shell
>>> from rides.models import Ride
>>> Ride.objects.all()  # ORM query
```

### Raw SQL queries (if needed)
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM rides_ride WHERE status = %s", ['OPEN'])
rows = cursor.fetchall()
```
