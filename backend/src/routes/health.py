from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import get_db


probe_router = APIRouter()

@probe_router.get("/live")
def get_liveness():
    """Liveness проба приложения."""
    return {"status": "ok"}

@probe_router.get("/ready")
def get_readiness_probe(response: Response, db: Session = Depends(get_db)):
    """Readiness проба приложения."""

    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready"}
