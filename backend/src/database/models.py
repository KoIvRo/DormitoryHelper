from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Base(DeclarativeBase):
    """Класс для ORM базы данных."""

    pass


class User(Base):
    """Модель аккаунта пользователя в базе данных."""

    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True, index=True)
    name = Column(String(20))
    email = Column(String(30))
    password = Column(String(256))

    announcements = relationship(
        "Announcement", back_populates="user", cascade="all, delete-orphan"
    )


class Announcement(Base):
    """Размещенное объявление."""

    __tablename__ = "announcements"
    id = Column(Integer(), primary_key=True, autoincrement=True, index=True)
    name = Column(String(64))
    link = Column(String(64))
    category = Column(String(64))
    date = Column(DateTime())
    end_date = Column(DateTime())
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="announcements")
