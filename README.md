# DormitoryHelper

## Project Structure

```
dormitory-helper/
├── backend/
│   ├── src/
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── Dockerfile
├── announcement-app/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── README.md
```

## About

DormitoryHelper is a web application for managing announcements in student dormitories. The system consists of backend API and frontend React application.

## Backend

The backend provides REST API for user authentication and announcement management.
Authentication made with PyJWT and redis for token in blacklist.

### Backend Technology Stack

* Python 3.12
* FastAPI
* SQLite
* SQLAlchemy
* PyJWT
* Poetry for dependency management
* redis

## Frontend

The frontend is a React SPA (Single Page Application) with minimalistic design.

### Frontend Technology Stack

* React 20
* React Router DOM
* Axios for HTTP requests
* CSS

## Docker Setup

The project supports two modes of operation: development and production.

### Development Mode

In development mode, frontend and backend run as separate services with hot reloading.

Start development mode:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

Services:
* Frontend: http://localhost:3000
* Backend: http://localhost:8000

Features:
* Hot Module Replacement for frontend
* File system mounted into containers

### Production Mode

In production mode, frontend is built into static files.

Start production mode:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

Services:
* Frontend: http://localhost:3000
* Backend: http://localhost:8000

Features:
* Frontend optimized production build
* Files copied into containers

### Made by

* Korotaev Ivan