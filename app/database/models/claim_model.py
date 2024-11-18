from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from .base_model import BaseModel


class ClaimModel(BaseModel):
    __tablename__ = "claims"

    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    user_id = mapped_column(ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="claims")

    def to_dict(self) -> dict:
        response = super().to_dict()
        if self.user:
            response["user"] = self.user.to_dict()

        return response
