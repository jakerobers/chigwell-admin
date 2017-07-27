env:

```
export SECRET_KEY="supersecret"
export ADMIN_EMAIL="test@test.com"
export ADMIN_PASSWORD="test"
export LEDGER_FILE="/path/to/ledger.ledger"
export FLASK_APP="main.py"
```

Running:

```
source env && flask run --host=0.0.0.0
```
