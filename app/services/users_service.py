import logging
from typing import List

from app.schemas.users_schema import UserRequest, UserResponse, NewUserRequest
from app.exceptions import NotFound
from app.repository import UsersRepository

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
