from datetime import datetime, timedelta
from app.configs import settings

import jwt

class JWTHandler:
    def __init__(self) -> None:
        self.secret_key: str = settings.JWT_SECRET_KEY
        self.algorithm: str = settings.JWT_ALGORITHM
        self.expires_delta: timedelta = timedelta(minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
        
    def encode(self, data: dict) -> str:
        payload = data.copy()
        expire = datetime.now() + self.expires_delta
        payload.update(exp=expire)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def decode(self, token: str) -> str:
        pass
    
jwt_handler = JWTHandler()