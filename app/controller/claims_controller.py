from typing import List

from fastapi import HTTPException

from app.schemas.claims_schema import NewClaimRequest, ClaimRequest, ClaimResponse
from app.exceptions import BaseHTTPException, InternalServerError, NotFound
from app.services import ClaimsService


class ClaimsController:
    def __init__(self):
        self.service = ClaimsService()

    def create(self, new_claim: NewClaimRequest) -> ClaimResponse:
        try:
            return self.service.create(new_claim)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.create
            raise InternalServerError("algo salio mal")

    def get_list(self, limit: int, offset: int) -> List[ClaimResponse]:
        try:
            return self.service.get_list(limit, offset)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.get_list
            raise InternalServerError("algo salio mal")


    def get_by_id(self, id: int) -> ClaimResponse:
        try:
            return self.service.get_by_id(id)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.get_by_id
            raise InternalServerError("algo salio mal")

    def update(self, id: int, new_data: ClaimRequest) -> ClaimResponse:
        try:
            return self.service.update(id, new_data)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.update
            raise InternalServerError("algo salio mal")

    def delete(self, id: int) -> None:
        try:
            self.service.delete(id)
        except BaseHTTPException as ex:
            # TODO: implementar logging
            raise ex
        except Exception:
            # TODO log: Error no contemplado en ClaimsController.delete
            raise InternalServerError("algo salio mal")
