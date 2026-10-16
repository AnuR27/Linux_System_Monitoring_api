# System Monitoring API

A Python backend application that collects Linux system metrics, evaluates monitoring snapshots, and exposes system health data through a REST API. Built with FastAPI, PostgreSQL, SQLAlchemy, Docker Compose, and pytest.

The project demonstrates backend development practices including separation of concerns, repository patterns, scheduled background tasks, persistent storage, and automated testing.

## Features

- Collect CPU, memory, disk, and process metrics using `psutil`.
- Periodically collect metrics using a background scheduler.
- Classify monitoring snapshots by collection status and severity.
- Expose health, latest metrics, historical snapshots, and recorded errors through REST endpoints.
- Persist monitoring snapshots and errors in PostgreSQL.
- Use SQLAlchemy for database access.
- Run the API and database with Docker Compose.
- Test application logic and database repositories with pytest.

## Tech Stack

- **Python 3.12**
- **FastAPI** and **Uvicorn**
- **Pydantic**
- **psutil**
- **PostgreSQL 16**
- **SQLAlchemy** and **Psycopg**
- **Docker** and **Docker Compose**
- **pytest** and **HTTPX**

## Architecture

The application separates system collection, metric processing, persistence, scheduling, and HTTP handling.

- **Collector:** gathers system metrics.
- **Services:** processes collected metrics and records monitoring results.
- **Repositories:** handle snapshot and error persistence.
- **Scheduler:** triggers monitoring cycles at a configurable interval.
- **API routes:** expose health, metrics, and error information.
- **Database layer:** configures SQLAlchemy and initializes the database tables.

## Project Structure

```text
app/
├── api/
│   └── routes/
├── collector/
├── core/
├── models/
├── repository/
├── scheduler/
├── services/
└── main.py

tests/
Dockerfile
docker-compose.yml
requirements.txt
```

## Getting Started

### Prerequisites

- Docker Engine
- Docker Compose plugin

### Run with Docker Compose

Clone the repository:

```bash
git clone https://github.com/AnuR27/job_processing_and_monitoring_api.git
cd job_processing_and_monitoring_api
```

Build and start the API and database:

```bash
sudo docker compose up --build -d
```

Check the service status:

```bash
sudo docker compose ps
```

Check the API health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

View application logs:

```bash
sudo docker compose logs api --tail=50
```

Stop the services:

```bash
sudo docker compose down
```

The PostgreSQL data is stored in a named Docker volume so it can persist when containers are stopped or recreated. Do not use `docker compose down -v` unless you intentionally want to remove the database volume.

### Configuration

The application supports these environment variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy database connection URL |
| `MONITORING_INTERVAL_SECONDS` | Time between monitoring cycles |

The Compose configuration supplies the database connection and monitoring interval for the containerized application.

**Security note:** The credentials in the current Compose configuration are for local development only. Replace them with appropriately managed credentials before deploying to a shared or production environment.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Basic service message |
| `GET` | `/health` | Health check |
| `GET` | `/metrics/latest` | Latest monitoring snapshot |
| `GET` | `/metrics/history?limit=10` | Recent monitoring snapshots |
| `GET` | `/errors?limit=10` | Recent recorded monitoring errors |

Interactive API documentation is available at `http://127.0.0.1:8000/docs` while the application is running.

## Running Tests

Create a local virtual environment if you want to run the test suite outside Docker:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

The project currently has 33 passing tests. Database integration tests may require a reachable PostgreSQL instance with the expected test configuration.

## Current Status

The initial version includes scheduled system monitoring, REST endpoints, PostgreSQL persistence, Docker Compose support, and automated tests.

## Future Improvements

- Manage database schema changes with Alembic migrations.
- Improve configuration and secret management.
- Add continuous integration with GitHub Actions.
- Improve observability and operational documentation.
- Expand integration and failure-recovery tests.

## License

No license has been selected yet.
