import logging

from fastapi import APIRouter, Request, Depends, HTTPException
from database.models import User, Announcement
from sqlalchemy.orm import Session
from database.database import get_db
from logging_config import log_fields

user_router = APIRouter()
logger = logging.getLogger("dormitory_helper.users")


@user_router.get("/me")
async def me(request: Request, db: Session = Depends(get_db)):
    """Получения полной информации о пользователе."""
    request_user = request.state.user

    exsiting_user = db.query(User).filter(User.id == request_user["user_id"]).first()
    if not exsiting_user:
        logger.warning(
            "Получение профиля отклонено: пользователь не найден",
            extra=log_fields(
                event="user.profile_lookup.rejected",
                outcome="failure",
                reason="user_not_found",
                request_id=request.state.request_id,
                user_id=request_user["user_id"],
            ),
        )
        raise HTTPException("Invalid token")

    announcement = (
        db.query(Announcement).filter(Announcement.user_id == exsiting_user.id).all()
    )

    logger.info(
        "Получена информация о пользователе",
        extra=log_fields(
            event="user.profile_retrieved",
            outcome="success",
            request_id=request.state.request_id,
            user_id=exsiting_user.id,
            announcement_count=len(announcement),
        ),
    )

    return {
        "id": exsiting_user.id,
        "email": exsiting_user.email,
        "name": exsiting_user.name,
        "announcement": announcement,
    }
