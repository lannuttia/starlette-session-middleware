# Starlette Session Middleware

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
