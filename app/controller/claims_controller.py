import logging
from typing import List

from fastapi import HTTPException

from app.schemas.claims_schema import NewClaimRequest, ClaimRequest, ClaimResponse
from app.exceptions import BaseHTTPException, InternalServerError, NotFound
from app.services import ClaimsService


logger = logging.getLogger(__name__)


class ClaimsController:
    def __init__(self):
        self.service = ClaimsService()

    def create(self, new_claim: NewClaimRequest) -> ClaimResponse:
        try:
            logger.debug(f"Nuevo reclamo: {new_claim}")
            return self.service.create(new_claim)
        except BaseHTTPException as ex:
            logger.error(f'Error al procesar request, status code {ex.status_code}: {ex.description}')
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f'Error no contemplado en {__name__}.create()')
            raise InternalServerError("algo salio mal")

    def get_list(self, limit: int, offset: int) -> List[ClaimResponse]:
        try:
    
            return self.service.get_list(limit, offset)
        except BaseHTTPException as ex:
            print("asd")
            logger.error(f'Error al procesar request, status code {ex.status_code}: {ex.description}')
            self.__handler_http_exception(ex)
        except Exception as ex:
            print(ex)
            logger.critical(f'Error no contemplado en {__name__}.get_list()')
            raise InternalServerError("algo salio mal")

    def get_by_id(self, id: int) -> ClaimResponse:
        try:
            return self.service.get_by_id(id)
        except BaseHTTPException as ex:
            logger.error(f'Error al procesar request, status code {ex.status_code}: {ex.description}')
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f'Error no contemplado en {__name__}.get_by_id()')
            raise InternalServerError("algo salio mal")

    def update(self, id: int, new_data: ClaimRequest) -> ClaimResponse:
        try:
            return self.service.update(id, new_data)
        except BaseHTTPException as ex:
            logger.error(f'Error al procesar request, status code {ex.status_code}: {ex.description}')
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f'Error no contemplado en {__name__}.update()')
            raise InternalServerError("algo salio mal")

    def delete(self, id: int) -> None:
        try:
            self.service.delete(id)
        except BaseHTTPException as ex:
            logger.error(f'Error al procesar request, status code {ex.status_code}: {ex.description}')
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f'Error no contemplado en {__name__}.delete()')
            raise InternalServerError("algo salio mal")

    def __handler_http_exception(self, ex: BaseHTTPException) -> HTTPException:
        if ex.status_code >= 500:
            logger.critical(
                f"Error en el servidor con status code {ex.status_code}: {ex.description}"
            )
        else:
            logger.error(f"Error {ex.status_code}: {ex.description}")
            
        raise ex

