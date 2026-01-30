from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User, Announcement
from .models import AnnouncementtCreate


announcement_router = APIRouter()


@announcement_router.get("/")
async def announcement(request: Request, db: Session = Depends(get_db)):
    """Все объявления."""
    announcement = db.query(Announcement).all()

    return {"account": announcement}


@announcement_router.get("/category/{category}")
async def announcement_category(category: str, request: Request, db: Session = Depends(get_db)):
    """Объявления по категории."""
    announcement = (
        db.query(Announcement).filter(Announcement.category == category).all()
    )

    if not announcement:
        raise HTTPException(status_code=404)

    return {"account": announcement}


@announcement_router.get("/{id}")
async def account(id: int, request: Request, db: Session = Depends(get_db)):
    """Информация об обявлении."""
    announcement = db.query(Announcement).filter(Announcement.id == id).first()

    if not announcement:
        raise HTTPException(status_code=404)

    return {"account": announcement}


@announcement_router.post("/")
async def create_account(
    data: AnnouncementtCreate, request: Request, db: Session = Depends(get_db)
):
    """Создание объявления."""
    request_user = request.state.user

    exsiting_user = db.query(User).filter(User.id == request_user["user_id"]).first()
    if not exsiting_user:
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

    return {"account": new_announcement}


@announcement_router.delete("/{id}")
async def delete_account(id: int, request: Request, db: Session = Depends(get_db)):
    """Удаление объявления."""
    request_user = request.state.user

    announcement = db.query(Announcement).filter(Announcement.id == id).first()

    if not announcement:
        raise HTTPException(status_code=404)

    if announcement.user_id != request_user["user_id"]:
        raise HTTPException(status_code=401)

    db.delete(announcement)
    db.commit()

    return {"detail": "announcement deleted"}
