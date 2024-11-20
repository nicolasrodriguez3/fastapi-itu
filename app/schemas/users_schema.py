from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.enums import RoleEnum


class NewUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: RoleEnum = RoleEnum.USER


class UserRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    role: RoleEnum | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class ClaimUserResponse(BaseModel):
    username: str
    role: RoleEnum
