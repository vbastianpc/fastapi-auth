# fastapi-auth

FastAPI implementation with identification and authentication system using JWT and SQLAlchemy.

## Installation

Require python 3.11

Create new environment.

```console
$ python -m venv venv
$ source ./venv/bin/activate
```

Install dependencies.

```console
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Run

```console
$ uvicorn app.main:app --host 0.0.0.0 --port 8000
```

or

```console
$ python -m app.main
```
