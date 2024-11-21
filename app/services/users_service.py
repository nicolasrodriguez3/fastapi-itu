import logging
from typing import List

from app.exceptions.client_exceptions import BadRequest
from app.schemas.auth_schemas import DecodedJwt
from app.schemas.users_schema import UserRequest, UserResponse, NewUserRequest
from app.exceptions import NotFound
from app.repository import UsersRepository
from app.enums import RoleEnum, ROLE_LEVELS

logger = logging.getLogger(__name__)


class UsersService:
    def __init__(self):
        self.__users_repo = UsersRepository()

    def create(self, new_user: NewUserRequest) -> UserResponse:
        user_dict = self.__users_repo.create(new_user.model_dump())
        return UserResponse(**user_dict)

    def get_list(self, limit: int, offset: int) -> List[UserResponse]:
        users = self.__users_repo.get_list(limit, offset)
        return [UserResponse(**user) for user in users]

    def get_by_id(self, user_id: int) -> UserResponse:
        user = self.__users_repo.get_by_id(user_id)
        if user is None:
            raise NotFound(f"Usuario id {user_id} no encontrado")
        return UserResponse(**user)

    def update(self, user_id: int, new_data: UserRequest) -> UserResponse:
        updated_user = self.__users_repo.update(
            user_id, new_data.model_dump(exclude_none=True)
        )
        if updated_user is None:
            raise NotFound("Usuario no encontrado")
        return UserResponse(**updated_user)

    def delete(self, user_id: int) -> None:
        if not self.__users_repo.delete(user_id):
            raise NotFound("Usuario no encontrado")
        return

    def change_role(
        self, user_id_to_update: int, new_role: RoleEnum, user: DecodedJwt
    ) -> UserResponse:
        if user.user_id == user_id_to_update:
            raise BadRequest("No puedes cambiar tu propio rol")

        target_user = self.get_by_id(user_id_to_update)

        if target_user.role == new_role:
            raise BadRequest("No puedes cambiar el rol a uno igual al actual")

        target_user_role_level: int | None = ROLE_LEVELS.get(target_user.role)
        user_role_level: int | None = ROLE_LEVELS.get(user.role)

        if target_user_role_level is None or user_role_level is None:
            raise BadRequest("Rol no permitido")

        if target_user_role_level <= user_role_level:
            raise BadRequest(
                "No puedes cambiar el rol de un usuario con un rol igual o mayor que el tuyo"
            )

        return self.update(user_id_to_update, UserRequest(role=new_role))
