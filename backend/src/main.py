import uvicorn
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routes.auth import auth_router
from routes.user import user_router
from routes.announcements import announcement_router
from database.database import create_db
from middleware import JWTMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(JWTMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем запросы с React приложения
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(announcement_router, prefix="/announcements")

if os.path.exists("static"):
    app.mount(
        "/",
        StaticFiles(directory="static", html=True),
        name="static",
    )

def main() -> None:
    """Точка запуска REST API."""
    create_db()
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
