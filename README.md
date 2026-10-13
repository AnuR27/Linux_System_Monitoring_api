# Job Processing & System Monitoring API

A Python backend project built with FastAPI to monitor Linux system health and expose system metrics through a REST API. The project emphasizes clean architecture, error handling, automated testing, and maintainable backend design.

## Current Focus

The initial version focuses on collecting Linux system metrics, processing monitoring snapshots, and exposing health and metrics information through API endpoints.

### Planned Features

- Track job execution records and lifecycle states
- Add persistent storage with PostgreSQL
- Improve structured logging and application configuration
- Add integration tests and containerization with Docker

## Tech Stack

- **Python** — application logic
- **FastAPI** — REST API framework
- **Pydantic** — data validation and response models
- **psutil** — Linux system metrics collection
- **Uvicorn** — ASGI server
- **pytest** — automated testing

## Architecture

The application is organized into separate components:

- **Collector** — gathers CPU, memory, disk, and process metrics
- **Models** — define raw metrics, monitoring snapshots, and errors
- **Services** — process metrics and determine collection status
- **Repositories** — manage stored snapshots and associated errors
- **Scheduler** — coordinates periodic metric collection
- **API routes** — expose monitoring data and health information

This separation keeps system collection, business logic, storage, and HTTP handling independent and easier to test.

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
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AnuR27/job_processing_and_monitoring_api.git
cd job_processing_and_monitoring_api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run tests

```bash
python -m pytest -q
```

The API startup command and available endpoints will be documented once the application entry point and routes are implemented.

## Learning Goals

- Design and implement REST APIs with FastAPI
- Collect and process Linux system metrics
- Apply separation of concerns and repository patterns
- Handle partial failures and missing metric data
- Write automated unit tests with pytest
- Build toward a backend system that also tracks job execution

## Roadmap

- [x] Initialize project structure and development environment
- [x] Implement an in-memory snapshot repository with unit tests
- [ ] Implement system metrics collection
- [ ] Implement monitoring services and error tracking
- [ ] Expose metrics, history, and health endpoints
- [ ] Add periodic collection and application orchestration
- [ ] Add job execution tracking
- [ ] Add PostgreSQL persistence and integration tests
- [ ] Document API usage and deployment

## License

To be decided.
