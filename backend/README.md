## Backend

```bash

cd backend
```

```bash

$ python --version
```

-> "$ Python 3.11.9"

### Create local environment

```bash

python -m venv .venv
```

### Activate local environment

```bash

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

### Deploy backend to AWS

```bash

eb deploy
```
