from datetime import datetime

from pydantic import BaseModel

from .users_schema import ClaimUserResponse


class NewClaimRequest(BaseModel):
    description: str = ""
    status: str = "open"


class ClaimRequest(BaseModel):
    description: str | None = None
    status: str | None = None


class ClaimResponse(BaseModel):
    id: int
    description: str = ""
    status: str = "open"
    user_id: int
    user: ClaimUserResponse
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
