from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from .base_model import BaseModel


class ClaimModel(BaseModel):
    __tablename__ = "claims"
    
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    
    user_id = mapped_column(ForeignKey("users.id"))
    
    user = relationship("UserModel", back_populates="claims")