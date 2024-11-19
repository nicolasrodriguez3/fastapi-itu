from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.enums import RoleEnum
from .users_schema import UserResponse


class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: RoleEnum = RoleEnum.USER


class TokenResponse(BaseModel):
    access_token: str = ""
    token_type: str = "bearer"
    user: UserResponse


class LoginUser(BaseModel):
    username: str
    password: str


class DecodedJwt(BaseModel):
    user_id: int
    role: RoleEnum
    exp: datetime
