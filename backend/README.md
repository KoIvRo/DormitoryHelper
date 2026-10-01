# Backend for DormitoryHelper

## Local start

PostgreSQL must already be available. In the `backend` directory, set its connection parameters and the JWT secret, then run:

```
poetry install
cd src
POSTGRES_HOST=localhost JWT_SECRET_KEY=local-secret poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8000
```

For the reproducible full-stack start, use Docker Compose as described in the root `README.md`.

## Documentation

### Authentication
For authentication using JWT token.

### Endpoints

#### Authentication
* `POST /auth/register` (email: str, password: str, name: str)
* `POST /auth/login` (email: str, password: str)
* `POST /auth/refresh` - Refresh access token

#### User
* `GET /user/me` - Get current user info with announcements

#### Announcements
* `GET /announcements/` - Get all announcements
* `GET /announcements/category/{category}` - Get announcements by category
* `GET /announcements/{id}` - Get announcements by ID
* `POST /announcements/` - Create new announcements
* `PUT /announcements/{id}` - Update own announcement
* `DELETE /announcements/{id}` - Delete announcements

## Tools
* Python
* FastAPI
* uvicorn
* PostgreSQL
* SQLalchemy
* PyJWT

### Made by
* Korotaev Ivan
