# Backend for DormitoryHelper

## For start

In backend directory
```
poetry install
poetry run startserver
```

or

In src/
```
uvicorn main:app --reload --host=0.0.0.0 --port=8000
```

or with docker

In backend/
```
docker build -t backend .
docker run -p 8000:8000 backend
```

## Documentation

### Authentication
For authentication using JWT token.

### Endpoints

#### Authentication
* `POST /auth/register` (email: str, password: str, name: str)
* `POST /auth/login` (email: str, password: str)
* `POST /auth/logout`

#### User
* `GET /user/me` - Get current user info with announcements

#### Announcements
* `GET /announcements/` - Get all announcements
* `GET /announcements/category/{category}` - Get announcements by category
* `GET /announcements/{id}` - Get announcements by ID
* `POST /announcements/` - Create new announcements
* `DELETE /announcements/{id}` - Delete announcements

## Tools
* Python
* FastAPI
* uvicorn
* SQLite
* SQLalchemy
* PyJWT

### Made by
* Korotaev Ivan
