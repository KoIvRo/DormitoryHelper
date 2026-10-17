import logging

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User, Announcement
from .models import AnnouncementCreate
from logging_config import log_fields

announcement_router = APIRouter()
logger = logging.getLogger("dormitory_helper.announcements")


@announcement_router.get("/")
async def announcement(request: Request, db: Session = Depends(get_db)):
    """Все объявления."""
    announcement = db.query(Announcement).all()

    logger.info(
        "Получен список объявлений",
        extra=log_fields(
            event="announcement.listed",
            outcome="success",
            request_id=request.state.request_id,
            user_id=request.state.user["user_id"],
            result_count=len(announcement),
        ),
    )

    return {"account": announcement}


@announcement_router.get("/category/{category}")
async def announcement_category(
    category: str, request: Request, db: Session = Depends(get_db)
):
    """Объявления по категории."""
    announcement = (
        db.query(Announcement).filter(Announcement.category == category).all()
    )

    if not announcement:
        logger.warning(
            "Объявления указанной категории не найдены",
            extra=log_fields(
                event="announcement.category_list.rejected",
                outcome="failure",
                reason="not_found",
                request_id=request.state.request_id,
                user_id=request.state.user["user_id"],
                category=category,
            ),
        )
        raise HTTPException(status_code=404)

    logger.info(
        "Получен список объявлений по категории",
        extra=log_fields(
            event="announcement.category_listed",
            outcome="success",
            request_id=request.state.request_id,
            user_id=request.state.user["user_id"],
            category=category,
            result_count=len(announcement),
        ),
    )

    return {"account": announcement}


@announcement_router.get("/{id}")
async def account(id: int, request: Request, db: Session = Depends(get_db)):
    """Информация об обявлении."""
    announcement = db.query(Announcement).filter(Announcement.id == id).first()

    if not announcement:
        logger.warning(
            "Объявление не найдено",
            extra=log_fields(
                event="announcement.lookup.rejected",
                outcome="failure",
                reason="not_found",
                request_id=request.state.request_id,
                user_id=request.state.user["user_id"],
                announcement_id=id,
            ),
        )
        raise HTTPException(status_code=404)

    logger.info(
        "Получена информация об объявлении",
        extra=log_fields(
            event="announcement.retrieved",
            outcome="success",
            request_id=request.state.request_id,
            user_id=request.state.user["user_id"],
            announcement_id=announcement.id,
            announcement_owner_id=announcement.user_id,
            category=announcement.category,
        ),
    )

    return {"account": announcement}


@announcement_router.post("/")
async def create_account(
    data: AnnouncementCreate, request: Request, db: Session = Depends(get_db)
):
    """Создание объявления."""
    request_user = request.state.user

    exsiting_user = db.query(User).filter(User.id == request_user["user_id"]).first()
    if not exsiting_user:
        logger.warning(
            "Создание объявления отклонено: пользователь не найден",
            extra=log_fields(
                event="announcement.creation.rejected",
                outcome="failure",
                reason="user_not_found",
                request_id=request.state.request_id,
                user_id=request_user["user_id"],
                category=data.category,
            ),
        )
        raise HTTPException(status_code=401)

    new_announcement = Announcement(
        name=data.name,
        link=data.link,
        category=data.category,
        date=data.date,
        end_date=data.end_date,
        user_id=exsiting_user.id,
    )

    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)

    logger.info(
        "Объявление создано",
        extra=log_fields(
            event="announcement.created",
            outcome="success",
            request_id=request.state.request_id,
            user_id=exsiting_user.id,
            announcement_id=new_announcement.id,
            category=new_announcement.category,
            starts_at=new_announcement.date,
            ends_at=new_announcement.end_date,
        ),
    )

    return {"account": new_announcement}


@announcement_router.put("/{id}")
async def update_announcement(
    id: int,
    data: AnnouncementCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Полное обновление объявления его владельцем."""
    announcement = db.query(Announcement).filter(Announcement.id == id).first()

    if not announcement:
        logger.warning(
            "Обновление объявления отклонено: объявление не найдено",
            extra=log_fields(
                event="announcement.update.rejected",
                outcome="failure",
                reason="not_found",
                request_id=request.state.request_id,
                user_id=request.state.user["user_id"],
                announcement_id=id,
            ),
        )
        raise HTTPException(status_code=404, detail="Announcement not found")

    if announcement.user_id != request.state.user["user_id"]:
        logger.warning(
            "Обновление объявления отклонено: пользователь не является владельцем",
            extra=log_fields(
                event="announcement.update.rejected",
                outcome="failure",
                reason="not_owner",
                request_id=request.state.request_id,
                user_id=request.state.user["user_id"],
                announcement_id=id,
                announcement_owner_id=announcement.user_id,
            ),
        )
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for field, value in data.model_dump().items():
        setattr(announcement, field, value)

    db.commit()
    db.refresh(announcement)

    logger.info(
        "Объявление обновлено",
        extra=log_fields(
            event="announcement.updated",
            outcome="success",
            request_id=request.state.request_id,
            user_id=request.state.user["user_id"],
            announcement_id=announcement.id,
            category=announcement.category,
            changed_fields=sorted(data.model_dump().keys()),
        ),
    )

    return {"account": announcement}


@announcement_router.delete("/{id}")
async def delete_account(id: int, request: Request, db: Session = Depends(get_db)):
    """Удаление объявления."""
    request_user = request.state.user

    announcement = db.query(Announcement).filter(Announcement.id == id).first()

    if not announcement:
        logger.warning(
            "Удаление объявления отклонено: объявление не найдено",
            extra=log_fields(
                event="announcement.deletion.rejected",
                outcome="failure",
                reason="not_found",
                request_id=request.state.request_id,
                user_id=request_user["user_id"],
                announcement_id=id,
            ),
        )
        raise HTTPException(status_code=404)

    if announcement.user_id != request_user["user_id"]:
        logger.warning(
            "Удаление объявления отклонено: пользователь не является владельцем",
            extra=log_fields(
                event="announcement.deletion.rejected",
                outcome="failure",
                reason="not_owner",
                request_id=request.state.request_id,
                user_id=request_user["user_id"],
                announcement_id=id,
                announcement_owner_id=announcement.user_id,
            ),
        )
        raise HTTPException(status_code=403, detail="Not enough permissions")

    deleted_category = announcement.category
    db.delete(announcement)
    db.commit()

    logger.info(
        "Объявление удалено",
        extra=log_fields(
            event="announcement.deleted",
            outcome="success",
            request_id=request.state.request_id,
            user_id=request_user["user_id"],
            announcement_id=id,
            category=deleted_category,
        ),
    )

    return {"detail": "announcement deleted"}
