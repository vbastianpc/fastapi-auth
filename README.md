# fastapi-auth

FastAPI implementation with identification and authentication system using JWT and SQLAlchemy.

## Installation

Require python 3.11

Create and start virtual environment

```console
python -m venv venv
source ./venv/bin/activate
```

Install dependencies

```console
pip install --upgrade pip
pip install -r requirements.txt
```

## Run

With uvicorn

```console
uvicorn app.main:app --host 0.0.0.0 --port 80
```

With gunicorn

```console
gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

Python file

```console
python -m app.main
```
