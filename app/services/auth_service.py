import logging

from app.schemas import (
    RegisterNewUser,
    LoginUser,
    TokenResponse,
    UserResponse,
    NewUserRequest,
)
from app.exceptions import BadRequest
from app.repository import UsersRepository
from app.services import UsersService
from app.handlers import jwt_handler
from app.enums import RoleEnum as Role

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.user_service = UsersService()
        self.user_repo = UsersRepository()

    def register(self, new_user: RegisterNewUser) -> TokenResponse:
        new_user_dict = new_user.model_dump()
        new_user_dict.update(role=Role.USER)
        user = self.user_service.create(NewUserRequest(**new_user_dict))
        return self.__get_token(user)

    def login(self, credentials: LoginUser) -> TokenResponse:
        user = self.user_repo.get_by_username(credentials.username)
        if not user:
            raise BadRequest("Credenciales incorrectas")
        if not self.check_password(user["id"], credentials.password):
            raise BadRequest("Credenciales incorrectas")

        response = TokenResponse.model_validate({"user": user})
        response.access_token = self.__get_user_token(
            response.user.id, response.user.role
        )
        return response

    def check_password(self, user_id: int, password: str) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        return self.user_repo.check_password(user_id, password)

    def __get_token(self, user: UserResponse) -> TokenResponse:
        token = self.__get_user_token(user.id, user.role)
        return TokenResponse(access_token=token, user=user)

    def __get_user_token(self, user_id: int, user_role) -> str:
        payload = {
            "user_id": str(user_id),
            "role": user_role,
        }
        return jwt_handler.encode(payload)
