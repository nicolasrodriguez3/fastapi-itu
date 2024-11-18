from typing import List
from sqlalchemy.exc import IntegrityError

from app.database import database_connection
from app.database.models import UserModel
from app.exceptions import UniqueFieldException


class UsersRepository:
    def __init__(self):
        self.db = database_connection.session

    def create(self, new_user_dict: dict) -> dict:
        new_user = UserModel(**new_user_dict)
        self.db.add(new_user)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise UniqueFieldException(e.args)

        self.db.refresh(new_user)
        return new_user.to_dict()

    def get_list(self, limit: int, offset: int) -> List[dict]:
        users = (
            self.db.query(UserModel).order_by("id").limit(limit).offset(offset).all()
        )
        return [user.to_dict() for user in users]

    def get_by_id(self, user_id: int) -> dict | None:
        user = self.__get_one(user_id)
        if user is None:
            return None
        return user.to_dict

    def update(self, user_id: int, new_data: dict) -> dict | None:
        user = self.__get_one(user_id)
        if user is None:
            return None
        for key, value in new_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user.to_dict

    def delete(self, user_id: int) -> bool:
        user = self.__get_one(user_id)
        if user is None:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def check_password(self, user_id: int, password: str):
        user = self.__get_one(user_id)
        if not user:
            return False
        return user.check_password(password)

    def __get_one(self, user_id: int) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
