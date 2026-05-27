# Job Monitor API

A lightweight backend API built with FastAPI for managing and tracking job execution data. The project focuses on backend architecture, validation, and clean separation of concerns.

---

## Features

* Create and retrieve job records
* Track job status (success, failed, running)
* Input validation using Pydantic models
* Structured API responses with response models
* Modular architecture with separation of routing, services, and schemas
* Error handling using HTTP exceptions

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

---

## Project Structure

```
app/
├── main.py
├── routers/
├── schemas/
├── services/
├── data/
└── core/
```

---

## Architecture Overview

The application follows a layered architecture:

* **Routers** → Handle HTTP requests and define API endpoints
* **Schemas** → Define data validation and API contracts
* **Services** → Contain business logic and processing rules
* **Data Layer** → Stores and manages sample or persistent data

This separation improves maintainability, scalability, and clarity of the codebase.

---

## Running the Project

```bash
uvicorn app.main:app --reload
```

API documentation available at:

```
http://127.0.0.1:8000/docs
```

---

## Learning Goals

This project was built to strengthen understanding of:

* Backend API design
* FastAPI architecture
* Data validation and response modeling
* Separation of concerns in backend systems
* Clean project structuring practices

---

## Future Improvements

* Add PostgreSQL database integration
* Add authentication system (JWT)
* Add unit and integration tests
* Containerize using Docker
* Improve logging and configuration management
