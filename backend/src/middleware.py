from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from security.jwt_utils import verify_jwt


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки токенов."""

    PUBLIC_PATHS = (
        "/docs",
        "/auth/register",
        "/auth/login",
        "/openapi.json",
        "/auth/refresh",
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
            return JSONResponse(
                {"code": 401, "detail": "Token not exist"}, status_code=401
            )

        payload = verify_jwt(access_token)

        if not payload or payload["type"] != "access":
            return JSONResponse(
                {"code": 401, "detail": "Invalid token"}, status_code=401
            )

        request.state.user = payload
        return await call_next(request)
