import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from .models import UserRegistration, UserLogin
from security.pass_utils import get_pass_hash, verify_pass
from security.jwt_utils import create_access_token, create_refresh_token, verify_jwt
from logging_config import log_fields
from metrics import USER_LOGINS, USER_REGISTRATIONS

auth_router = APIRouter()
logger = logging.getLogger("dormitory_helper.auth")


@auth_router.post("/register")
async def register(
    user_data: UserRegistration, request: Request, db: Session = Depends(get_db)
):
    """Эндпоинт для регистрации."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(
            "Регистрация отклонена: пользователь уже существует",
            extra=log_fields(
                event="user.registration.rejected",
                outcome="failure",
                reason="email_already_registered",
                request_id=request.state.request_id,
                user_id=existing_user.id,
            ),
        )
        raise HTTPException(status_code=400)

    hashed_password = get_pass_hash(user_data.password)

    new_user = User(
        name=user_data.name, email=user_data.email, password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    USER_REGISTRATIONS.inc()

    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    logger.info(
        "Пользователь зарегистрирован",
        extra=log_fields(
            event="user.registered",
            outcome="success",
            request_id=request.state.request_id,
            user_id=new_user.id,
        ),
    )

    return {"access": access_token, "refresh": refresh_token}


@auth_router.post("/login")
async def login(user_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Эндпоинт для логина."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if not existing_user:
        USER_LOGINS.labels(outcome="failure").inc()
        logger.warning(
            "Вход отклонён: пользователь не найден",
            extra=log_fields(
                event="user.login.rejected",
                outcome="failure",
                reason="user_not_found",
                request_id=request.state.request_id,
            ),
        )
        raise HTTPException(status_code=400)

    if not verify_pass(user_data.password, existing_user.password):
        USER_LOGINS.labels(outcome="failure").inc()
        logger.warning(
            "Вход отклонён: неверный пароль",
            extra=log_fields(
                event="user.login.rejected",
                outcome="failure",
                reason="invalid_password",
                request_id=request.state.request_id,
                user_id=existing_user.id,
            ),
        )
        raise HTTPException(status_code=400)

    access_token = create_access_token(existing_user.id)
    refresh_token = create_refresh_token(existing_user.id)

    USER_LOGINS.labels(outcome="success").inc()

    logger.info(
        "Пользователь вошёл в систему",
        extra=log_fields(
            event="user.logged_in",
            outcome="success",
            request_id=request.state.request_id,
            user_id=existing_user.id,
        ),
    )

    return {"access": access_token, "refresh": refresh_token}


@auth_router.post("/refresh")
async def refresh_token(request_data: dict, request: Request):
    """Обновление access токена по refresh токену."""
    refresh_token = request_data.get("refresh_token")
    if not refresh_token:
        logger.warning(
            "Обновление access-токена отклонено: отсутствует refresh-токен",
            extra=log_fields(
                event="token.refresh.rejected",
                outcome="failure",
                reason="token_missing",
                request_id=request.state.request_id,
            ),
        )
        raise HTTPException(status_code=401, detail="Refresh token required")

    payload = verify_jwt(refresh_token, "refresh")
    if not payload:
        logger.warning(
            "Обновление access-токена отклонено: некорректный refresh-токен",
            extra=log_fields(
                event="token.refresh.rejected",
                outcome="failure",
                reason="token_invalid",
                request_id=request.state.request_id,
            ),
        )
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(payload["user_id"])

    logger.info(
        "Access-токен обновлён",
        extra=log_fields(
            event="token.refreshed",
            outcome="success",
            request_id=request.state.request_id,
            user_id=payload["user_id"],
        ),
    )

    return {"access": new_access_token}
