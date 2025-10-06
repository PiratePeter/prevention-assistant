## Database

```bash

cd database
```

### Create local user and local database

```bash
psql -U postgres -c "CREATE USER gvbuser WITH LOGIN;"
psql -U postgres -c "CREATE DATABASE gvbdb OWNER gvbuser;"
```

### Init local database

```bash
psql -U gvbuser -d gvbdb -f schema.sql
```

### Init AWS database

Manually set public accessability to "Yes" and add an inbound rule with "My IP" as Source.

```bash
psql -h gvbdb.'<id>'.eu-central-1.rds.amazonaws.com -U gvbuser -d gvbdb -f schema.sql
```
