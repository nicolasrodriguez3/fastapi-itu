from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base_model import BaseModel


class ClaimModel(BaseModel):
    __tablename__ = "claims"
    
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)