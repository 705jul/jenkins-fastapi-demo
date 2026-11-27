# Jenkins FastAPI Demo

Jenkins CI/CD Training on AWS Cloud

## Application

- Python
- FastAPI
- Uvicorn

## API Endpoints

- GET /
- GET /health
- GET /api/v1/add
- GET /docs

## Development Environment

Create a Python virtual environment.

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies.

    python -m pip install -r requirements-dev.txt

## Run Application

    python -m uvicorn app:app --host 127.0.0.1 --port 8000

## Run Tests

    python -m pytest -v

## Generate Test Report

    mkdir -p reports
    python -m pytest -v --junitxml=reports/junit.xml
## Day 04 - Poll SCM
Jenkins periodically checks GitHub for source code changes.
## GitHub Webhook
GitHub automatically notifies Jenkins when changes are pushed.
## Version 1.1.0
New API endpoint:
- GET /api/v1/multiply
The application supports addition and multiplication.
