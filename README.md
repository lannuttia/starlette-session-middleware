# Starlette Session Middleware &middot; [![codecov](https://codecov.io/github/lannuttia/starlette-session-middleware/graph/badge.svg?token=2FO77C58EP)](https://codecov.io/github/lannuttia/starlette-session-middleware) [![Known Vulnerabilities](https://snyk.io/test/github/lannuttia/starlette-session-middleware/badge.svg)](https://snyk.io/test/github/lannuttia/starlette-session-middleware)

## Purpose
The purpose of this project is to provide an enhanced, more flexible ASGI session middleware

## Getting started

In the project root, you will want to create and activate a Python virtual environment in a folder called `.venv`.
On Fedora 38 this can be done by running `python3.9 -m venv .venv && source .venv/bin/activate`. You will then want to
pip install all of the dependencies for local development. This can be done by running `pip install -r requirements.txt`
in your Python 3.9 virtual environment. After that, you will want to run `pre-commit install` to install all of the
pre-commit hooks. This ensures that we reduce unneeded pipeline failures.

## Running the Tests

You can run the tests by running `python -m pytest -n auto --cov`. This will use pytest-xdist to parallelize the tests and provide a code
coverage report by using pytest-cov.

## Usage

### FastAPI
In order to use a JWT persisted with a cookie and passed through a cookie, you would create the middleware as follows.
```python
from fastapi import FastAPI
from starlette_session.middleware import SessionMiddleware
from starlette_session.middleware.codecbackends.jwt import JwtCodecBackend
from starlette_session.middleware.storagebackends.cookie import CookieStorageBackend
from starlette_session.middleware.authorizationbackends.cookie import CookieAuthorizationBackend


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    codec_backend=JwtCodecBackend(key="somesuperdupersecurekey")
    storage_backend=CookieStorageBackend()
    authorization_backend=CookieAuthorizationBackend()
)
```

In order to use a JWT persisted with a cookie and passed through the Authorization header, you would create the middleware as follows.
```python
from fastapi import FastAPI
from starlette_session.middleware import SessionMiddleware
from starlette_session.middleware.codecbackends.jwt import JwtCodecBackend
from starlette_session.middleware.storagebackends.cookie import CookieStorageBackend
from starlette_session.middleware.authorizationbackends.authorizationheader import AuthorizationHeaderAuthorizationBackend


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    codec_backend=JwtCodecBackend(key="somesuperdupersecurekey")
    storage_backend=CookieStorageBackend()
    authorization_backend=AuthorizationHeaderAuthorizationBackend()
)
```
