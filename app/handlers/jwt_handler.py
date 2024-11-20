import jwt, logging

from datetime import datetime, timedelta, timezone
from typing import Any
from app.configs import settings

from app.exceptions import Unauthorized
from app.enums import RoleEnum


logger = logging.getLogger("jwt_handler")


class JWTHandler:
    def __init__(self) -> None:
        self.secret_key: str = settings.JWT_SECRET_KEY
        self.algorithm: str = settings.JWT_ALGORITHM
        self.expires_delta: timedelta = timedelta(
            minutes=settings.JWT_EXPIRATION_TIME_MINUTES
        )

    def encode(self, data: dict) -> str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + self.expires_delta
        payload.update(exp=expire)
        return jwt.encode(payload, self.secret_key, self.algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token expirado")
        except (jwt.InvalidSignatureError, jwt.InvalidTokenError):
            raise Unauthorized("Token invalido")

    def generate_example_token(self, role: RoleEnum = RoleEnum.USER) -> str:
        expire = datetime.now(timezone.utc) + self.expires_delta
        return self.encode({"role": role, "user_id": 1, "exp": expire})


jwt_handler = JWTHandler()
