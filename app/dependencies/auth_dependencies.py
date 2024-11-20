import logging
from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.enums import RoleEnum as Role
from app.handlers import jwt_handler
from app.exceptions import Unauthorized, Forbidden
from app.schemas import DecodedJwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

logger = logging.getLogger("auth")


def has_permission(allowed_roles: List[Role] = []):
    async def get_token_payload(
        authorization: str = Depends(oauth2_scheme),
    ) -> DecodedJwt:
        try:
            payload = jwt_handler.decode(authorization)
            validate_payload(payload)

            user_role = payload.get("role")

            # Validar roles
            if len(allowed_roles) > 0 and user_role not in [
                role.value for role in allowed_roles
            ]:
                logger.warning(
                    f"Acceso denegado. Usuario id: {payload.get('user_id')} con rol '{user_role}' intentó acceder a un recurso protegido. Roles permitidos: {allowed_roles}"
                )
                raise Forbidden(
                    "El usuario no tiene permiso para acceder a este recurso"
                )
            return DecodedJwt(**payload)
        except InvalidTokenError as e:
            logger.error(f"Error al decodificar el token: {e}")
            raise Unauthorized("Token inválido")

    return get_token_payload


def validate_payload(payload: dict) -> None:
    if not payload.get("user_id") or not payload.get("role"):
        raise Unauthorized("Token inválido")
