import bcrypt

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    encrypted_password: Mapped[str] = mapped_column(String(100), nullable=False)

    claims = relationship("ClaimModel", back_populates="user")

    @property
    def password(self) -> str:
        return self.encrypted_password

    @password.setter
    def password(self, password: str) -> None:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.encrypted_password = hashed_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.encrypted_password.encode("utf-8")
        )

