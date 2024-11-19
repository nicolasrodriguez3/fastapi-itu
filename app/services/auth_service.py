import logging
from typing import List

from app.schemas import RegisterUser, LoginUser, TokenResponse, UserResponse
from app.exceptions import NotFound, BadRequest
from app.repository import UsersRepository
from app.services import UsersService
from app.handlers.jwt_handler import jwt_handler

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.user_service = UsersService()
        self.user_repo = UsersRepository()

    def register(self, new_user: RegisterUser) -> TokenResponse:
        user = self.user_service.create(new_user)
        return self.__get_token(user)

    def login(self, credentials: LoginUser) -> TokenResponse:
        user = self.user_repo.get_by_username(credentials.username)
        if not user:
            raise BadRequest("Credenciales incorrectas")
        if not self.check_password(credentials.username, credentials.password):
            raise BadRequest("Credenciales incorrectas")
        return self.__get_token(user)

    def check_password(self, user_id: int, password: str) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        return user.check_password(password)

    def __get_token(self, user: UserResponse) -> TokenResponse:
        payload = {
            "user_id": str(user.id),
            "role": user.role,
        }
        return jwt_handler.encode(payload)
