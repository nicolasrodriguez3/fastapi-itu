from typing import List

from fastapi import HTTPException

from app.schemas.claims_schema import NewClaimRequest, ClaimRequest, ClaimResponse
from app.exceptions import BaseHTTPException, InternalServerError, NotFound


class ClaimsController:
    def __init__(self):
        pass

    def create(self, new_claim: NewClaimRequest) -> ClaimResponse:
        try:
            # TODO: llamar a la capa de servicio para que gestione la acción correspondiente
            # Retornar data de ejemplo
            return ClaimResponse(id=1, **new_claim.model_dump())
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.create
            raise InternalServerError("algo salio mal")

    def get_list(self, limit: int, offset: int) -> List[ClaimResponse]:
        try:
            # TODO: llamar a la capa de servicio para que gestione la acción correspondiente
            # Retornar data de ejemplo
            return []
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.get_list
            raise InternalServerError("algo salio mal")


    def get_by_id(self, id: int) -> ClaimResponse:
        try:
            # Retornar data de ejemplo
            return ClaimResponse(id=id)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.get_by_id
            raise InternalServerError("algo salio mal")

    def update(self, id: int, new_data: ClaimRequest) -> ClaimResponse:
        try:
            # Retornar data de ejemplo
            return ClaimResponse(id=id)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.update
            raise InternalServerError("algo salio mal")

    def delete(self, id: int) -> None:
        pass
