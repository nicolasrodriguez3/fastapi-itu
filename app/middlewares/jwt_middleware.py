import time, logging

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint as Callback,
)

from app.configs import settings
from app.handlers import jwt_handler

logger = logging.getLogger(__name__)


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callback) -> Response:
        # Obtener el token de la request
        token = request.headers.get("Authorization")

        # Ejecutar el endpoint
        response: Response = await call_next(request)

        if not token or not token.startswith("Bearer "):
            return response

        # Renovar el token
        try:
            jwt: dict = jwt_handler.decode(token.split("Bearer ")[1])
            expired_timestamp = jwt["exp"]
            time_left: int = int(expired_timestamp) - int(time.time()) // 60

            if time_left < (settings.JWT_EXPIRATION_TIME_MINUTES // 2):
                del jwt["exp"]
                new_token = jwt_handler.encode(jwt)
                response.headers["renewed-token"] = new_token

        except Exception as ex:
            logger.error(str(ex))

        return response
