from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.enums import RoleEnum as Role
from app.handlers import jwt_handler
from app.exceptions import Unauthorized, Forbidden
from app.schemas import DecodedJwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def has_permission(allowed_roles: List[Role] = []):
    async def get_token_payload(authorization: str = Depends(oauth2_scheme)) -> DecodedJwt:
        try:
            payload = jwt_handler.decode(authorization)
            if len(allowed_roles) > 0 and payload["role"] not in [role.value for role in allowed_roles]:
                raise Forbidden("El usuario no tiene permiso para acceder a este recurso")
            return DecodedJwt(**payload)
        except InvalidTokenError:
            raise Unauthorized("Token inválido")
        
    return get_token_payload