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
psql -U gvbuser -d gvbdb -f schema.sql
```
