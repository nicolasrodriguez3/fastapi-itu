from typing import List

from app.schemas import ClaimRequest, ClaimResponse, NewClaimRequest
from app.exceptions import NotFound
from app.repository import ClaimsRepository


class ClaimsService:
    def __init__(self):
        self.claims_repo = ClaimsRepository()

    def create(self, new_claim: NewClaimRequest, user_id: int) -> ClaimResponse:
        new_claim_dict = new_claim.model_dump()
        new_claim_dict.update(user_id=user_id)
        claim_dict = self.claims_repo.create(new_claim_dict)
        return ClaimResponse(**claim_dict)

    def get_list(self, limit: int, offset: int, user_id: int) -> List[ClaimResponse]:
        claims = self.claims_repo.get_list(limit, offset, user_id)
        return [ClaimResponse(**claim) for claim in claims]

    def get_by_id(self, id: int) -> ClaimResponse:
        claim = self.claims_repo.get_by_id(id)
        if claim is None:
            raise NotFound("Reclamo no encontrado")
        return ClaimResponse(**claim)

    def update(self, id: int, new_data: ClaimRequest) -> ClaimResponse:
        updated_claim = self.claims_repo.update(
            id, new_data.model_dump(exclude_none=True)
        )
        if updated_claim is None:
            raise NotFound("Reclamo no encontrado")
        return ClaimResponse(**updated_claim)

    def delete(self, id: int) -> None:
        if not self.claims_repo.delete(id):
            raise NotFound("Reclamo no encontrado")
        return
