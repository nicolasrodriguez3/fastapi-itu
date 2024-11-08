from typing import List

from app.schemas.claims_schema import ClaimRequest, ClaimResponse, NewClaimRequest


class ClaimsService:
    
    
    
    def __init__(self):
        # todo: instanciar capa de repositorio
        pass

    def create(self, new_claim: NewClaimRequest) -> ClaimResponse:
        # TODO:
        #* 1. Recibir el objeto NewClaimRequest, convertirlo a diccionario y pasar al repositorio
        #* 2. Recibir la respuesta del repositorio y retornar el objeto ClaimResponse
        
        pass
    
    def get_list(self, limit: int, offset: int) -> List[ClaimResponse]:
        pass
    
    def get_by_id(self, id: int) -> ClaimResponse:
        pass
    
    def update(self, id: int, new_data: ClaimRequest) -> ClaimResponse:
        pass
    
    def delete(self, id: int) -> None:
        pass