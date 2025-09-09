# Postgres Data Generator

A Python-based data generator to populate multiple PostgreSQL tables with realistic test data. Designed to handle multiple databases and scalable to hundreds of tables.


## Features

- Supports multiple PostgreSQL databases
- Dynamically loads table-specific generators
- Handles UUIDs, timestamps, and enums safely
- Sanitizes strings to match database column lengths
- Fully compatible with SQLAlchemy 2.x
- Easy to add new tables: just create a new generator



## Requirements

- Python 3.11+
- PostgreSQL (any number of databases)
- Virtual environment recommended



## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd postgres-data-generator

## Create a virtual environment

```bash
python -m venv venv
```


## Activate the virtual environment

### Windows:
```bash
venv\Scripts\activate
```

### Linux/macOS:

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration
All database connections are configured in config/config.yaml:

```bash
databases:
  main_db:
    host: localhost
    port: 5432
    name: e_database
    user: admin
    password: admin123
  admin_db:
    host: localhost
    port: 5433
    name: admin_panel_db
    user: admin
    password: admin123

```

## Adding a new table
Create a new generator in data_generators/:

```bash
data_generators/<table_name>_generator.py
```

Implement a <TableName>Generator class with a generate() method that returns a dictionary matching the table columns
Example:

```bash
# data_generators/users_generator.py
import uuid
from faker import Faker
from datetime import datetime

fake = Faker()

class UsersGenerator:
    def generate(self):
        return {
            "id": str(uuid.uuid4()),
            "email": fake.email()[:255],
            "username": fake.user_name()[:150],
            "password_hash": fake.sha256(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone_number": fake.phone_number()[:20],
            "date_of_birth": fake.date_of_birth(),
            "gender": fake.random_element(["male", "female", "other"]),
            "profile_picture": fake.image_url(),
            "user_type": fake.random_element(["customer", "admin", "vendor", "staff"]),
            "is_active": True,
            "is_email_verified": True,
            "last_login_at": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "deleted_at": None,
            "auth_provider": fake.random_element(["local", "google", "facebook", "github"])[:50],
            "role_id": None,
            "timezone": fake.timezone()[:50],
            "language": fake.language_code()[:10],
        }

```

## Usage

Populate a table with generated data:

```bash
python main.py --db <database_key> --table <table_name> --rows <number_of_rows>
```

--db: Database key from config.yaml (main_db, admin_db, etc.)
--table: Table name (must match generator file)
--rows: Number of rows to insert (default 100)

Example:

```bash
python main.py --db main_db --table users --rows 50

```

## Notes

Ensure all generators respect database column types and lengths.
SQLAlchemy 2.x is used for DB operations.
Multiple databases are supported by adding entries in config.yaml.
For large-scale data generation, consider batching inserts to avoid memory issues.



