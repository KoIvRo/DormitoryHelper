import os
from fastapi import FastAPI
from routes.auth import auth_router
from routes.user import user_router
from routes.announcements import announcement_router
from routes.health import probe_router
from routes.demo import demo_router
from middleware import JWTMiddleware, RequestLoggingMiddleware
from logging_config import configure_logging
from metrics import configure_metrics
from fastapi.middleware.cors import CORSMiddleware

configure_logging()
app = FastAPI()

app.add_middleware(JWTMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(announcement_router, prefix="/announcements")
app.include_router(probe_router, prefix="/health")
app.include_router(demo_router, prefix="/demo")

configure_metrics(app)
