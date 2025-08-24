# prevention-assistant

Bärn Häckt 2025 - Preventa

## Backend

```bash

cd backend
source .venv/Scripts/activate
```

### Prepare local environment

```bash

pip install -r requirements.txt
```

### Generate model classes

```bash

source .env && sqlacodegen $DATABASE_URL --outfile generated/models.py
```

### Start local server

```bash

python app.py
```

Open http://localhost:5000/

### Format code

```bash
black .
...
```

### Lint code

```bash

pylint .
```

### Execute tests

```bash

pytest
```

## Database

```bash

cd database
```

### Create user and database

```bash
psql -U postgres -c "CREATE USER gvbuser WITH LOGIN;"
psql -U postgres -c "CREATE DATABASE gvbdb OWNER gvbuser;"
```

### Init database

```bash
cd database
psql -U gvbuser -d gvbdb -f schema.sql
```
