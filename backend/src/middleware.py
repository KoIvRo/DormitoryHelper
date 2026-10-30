import logging
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from security.jwt_utils import verify_jwt
from logging_config import log_fields

logger = logging.getLogger("dormitory_helper.http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Журналирование всех HTTP-запросов приложения."""

    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request.state.request_id = request_id
        started_at = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            logger.exception(
                "HTTP-запрос завершился необработанной ошибкой",
                extra=log_fields(
                    event="http.request.completed",
                    outcome="failure",
                    request_id=request_id,
                    **{
                        "http.request.method": request.method,
                        "url.path": request.url.path,
                        "http.response.status_code": 500,
                        "duration_ms": duration_ms,
                    },
                ),
            )
            raise

        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        status_code = response.status_code
        log_method = logger.warning if status_code >= 400 else logger.info
        log_method(
            "HTTP-запрос завершён",
            extra=log_fields(
                event="http.request.completed",
                outcome="success" if status_code < 400 else "failure",
                request_id=request_id,
                user_id=getattr(request.state, "user", {}).get("user_id"),
                **{
                    "http.request.method": request.method,
                    "url.path": request.url.path,
                    "http.response.status_code": status_code,
                    "duration_ms": duration_ms,
                },
            ),
        )
        response.headers["X-Request-ID"] = request_id
        return response


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки токенов."""

    PUBLIC_PATHS = (
        "/docs",
        "/auth/register",
        "/auth/login",
        "/openapi.json",
        "/auth/refresh",
        "/health/live",
        "/health/ready",
        "/metrics",
        "/demo/work",
    )

    async def dispatch(self, request, call_next):
        """Проверка входящего запроса."""
        if request.url.path in JWTMiddleware.PUBLIC_PATHS:
            return await call_next(request)

        access_token = None

        auth_headers = request.headers.get("Authorization")
        if auth_headers and auth_headers.startswith("Bearer "):
            access_token = auth_headers.split()[1]

        if not access_token:
            logger.warning(
                "Запрос отклонён: отсутствует access-токен",
                extra=log_fields(
                    event="authentication.rejected",
                    outcome="failure",
                    reason="token_missing",
                    request_id=getattr(request.state, "request_id", None),
                    **{"url.path": request.url.path},
                ),
            )
            return JSONResponse(
                {"code": 401, "detail": "Token not exist"}, status_code=401
            )

        payload = verify_jwt(access_token)

        if not payload or payload["type"] != "access":
            logger.warning(
                "Запрос отклонён: некорректный access-токен",
                extra=log_fields(
                    event="authentication.rejected",
                    outcome="failure",
                    reason="token_invalid",
                    request_id=getattr(request.state, "request_id", None),
                    **{"url.path": request.url.path},
                ),
            )
            return JSONResponse(
                {"code": 401, "detail": "Invalid token"}, status_code=401
            )

        request.state.user = payload
        return await call_next(request)
