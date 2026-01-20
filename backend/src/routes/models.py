from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal


class UserRegistration(BaseModel):
    """Модель для регистрации."""

    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    """Модель для логина."""

    email: EmailStr
    password: str


class AnnouncementtCreate(BaseModel):
    "Модель для создания объявления."

    name: str
    link: str
    category: Literal["transport", "sale", "hobby"]
    date: datetime
    end_date: datetime
