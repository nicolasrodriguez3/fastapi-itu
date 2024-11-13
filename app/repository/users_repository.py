from sqlalchemy.exc import IntegrityError

from app.database import database_connection
from app.database.models import UserModel
from app.exceptions import UniqueFieldException


class UsersRepository:
    def __init__(self):
        self.db = database_connection.session

    def create(self, new_user_dict: dict) -> dict:
        try:
            new_user = UserModel(**new_user_dict)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return self.__to_dict(new_user)
        except IntegrityError as e:
            raise UniqueFieldException(str(e))