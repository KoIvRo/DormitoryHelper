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

#### User
* `GET /user/me` - Get current user info with accounts and transactions

#### Announcements
* `GET /announcements/{id}` - Get announcements by ID
* `POST /announcements/` - Create new announcements
* `DELETE /announcements/{id}` - Delete announcements

## API Examples

### Authentication
```
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"mypassword123\",\"name\":\"Ivan\"}"
```
```
curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"mypassword123\"}"
```

### User
```
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MX0.n2bhlHwTGFpTx6W2WOeAw7_rQUhO1umGHiv9XYLOBxc" http://localhost:8000/user/me
```

### Announcements
```
curl -X POST "http://localhost:8000/announcements/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoiYWNjZXNzIn0.6sCAY8zwf8ucfZCDiGiYve8KgiZU7SLurxMK9o2hiSw" -d "{\"name\":\"Такси\",\"link\":\"+7912\",\"date\":\"2026-01-21T00:00:00\",\"end_date\":\"2026-01-21T10:00:00\"}"
```
```
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MX0.n2bhlHwTGFpTx6W2WOeAw7_rQUhO1umGHiv9XYLOBxc" http://localhost:8000/announcements/1
```
```
curl -X DELETE "http://localhost:8000/announcements/1" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MX0.n2bhlHwTGFpTx6W2WOeAw7_rQUhO1umGHiv9XYLOBxc"
```

## Tools
* Python
* FastAPI
* uvicorn
* SQLite
* SQLalchemy
* PyJWT

### Made by
* Korotaev Ivan
