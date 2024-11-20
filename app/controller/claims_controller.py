import logging
from typing import List

from fastapi import HTTPException

from app.schemas.auth_schemas import DecodedJwt
from app.schemas.claims_schema import NewClaimRequest, ClaimRequest, ClaimResponse
from app.exceptions import BaseHTTPException, InternalServerError, NotFound, Forbidden
from app.services import ClaimsService
from app.enums import ADMIN_ROLES


logger = logging.getLogger(__name__)


class ClaimsController:
    def __init__(self):
        self.service = ClaimsService()

    def create(self, new_claim: NewClaimRequest, user_id: int) -> ClaimResponse:
        try:
            logger.debug(f"Nuevo reclamo: {new_claim}")
            return self.service.create(new_claim, user_id)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.create()")
            raise InternalServerError("algo salio mal")

    def get_list(self, limit: int, offset: int, user_id: int) -> List[ClaimResponse]:
        try:
            return self.service.get_list(limit, offset, user_id)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception as ex:
            print(ex)
            logger.critical(f"Error no contemplado en {__name__}.get_list(): {str(ex)}")
            raise InternalServerError("algo salio mal")

    def get_by_id(self, id: int, token: DecodedJwt) -> ClaimResponse:
        try:
            claim = self.service.get_by_id(id)
            self.__verify_access(claim.user_id, token)
            return claim
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.get_by_id()")
            raise InternalServerError("algo salio mal")

    def update(
        self, id: int, new_data: ClaimRequest, token: DecodedJwt
    ) -> ClaimResponse:
        try:
            self.get_by_id(id, token)
            return self.service.update(id, new_data)

        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.update()")
            raise InternalServerError("algo salio mal")

    def delete(self, id: int, token: DecodedJwt) -> None:
        try:
            # Validar que el usuario sea el dueño
            self.get_by_id(id, token)
            return self.service.delete(id)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.delete()")
            raise InternalServerError("algo salio mal")

    def __handler_http_exception(self, ex: BaseHTTPException):
        if ex.status_code >= 500:
            logger.critical(
                f"Error en el servidor con status code {ex.status_code}: {ex.description}"
            )
        else:
            logger.error(f"Error {ex.status_code}: {ex.description}")

        raise ex

    def __verify_access(self, owner_id: int, token: DecodedJwt) -> None:
        if owner_id != token.user_id and token.role not in ADMIN_ROLES:
            raise Forbidden("No se permite acceder al recurso")
