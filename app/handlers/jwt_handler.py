from datetime import datetime, timedelta, timezone
from app.configs import settings

import jwt

from app.exceptions import Unauthorized

class JWTHandler:
    def __init__(self) -> None:
        self.secret_key: str = settings.JWT_SECRET_KEY
        self.algorithm: str = settings.JWT_ALGORITHM
        self.expires_delta: timedelta = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
        
    def encode(self, data: dict) -> str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + self.expires_delta
        payload.update(exp=expire)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def decode(self, token: str) -> str:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token expirado")
        except jwt.InvalidTokenError or jwt.InvalidSignatureError:
            raise Unauthorized("Token invalido")
    
jwt_handler = JWTHandler()