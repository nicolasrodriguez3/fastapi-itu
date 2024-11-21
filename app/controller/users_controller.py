import logging
from typing import List

from app.exceptions import (
    BadRequest,
    BaseHTTPException,
    InternalServerError,
    NotFound,
    UniqueFieldException,
)
from app.schemas.auth_schemas import DecodedJwt
from app.schemas.users_schema import UserRequest, NewUserRequest, UserResponse
from app.services import UsersService

from app.enums import RoleEnum


logger = logging.getLogger(__name__)


class UsersController:
    def __init__(self):
        self.service = UsersService()

    def create(self, new_user: NewUserRequest) -> UserResponse:
        try:
            logger.debug(f"Nuevo usuario: {new_user}")
            return self.service.create(new_user)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except UniqueFieldException as ex:
            logger.error(str(ex))
            raise BadRequest("Error: campos duplicados")
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.create()" + str(ex))
            raise InternalServerError("algo salio mal")

    def get_list(self, limit: int, offset: int) -> List[UserResponse]:
        try:

            return self.service.get_list(limit, offset)
        except BaseHTTPException as ex:
            print("asd")
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception as ex:
            print(ex)
            logger.critical(f"Error no contemplado en {__name__}.get_list()")
            raise InternalServerError("algo salio mal")

    def get_by_id(self, id: int) -> UserResponse:
        try:
            return self.service.get_by_id(id)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.get_by_id()")
            raise InternalServerError("algo salio mal")

    def update(self, id: int, new_data: UserRequest) -> UserResponse:
        try:
            return self.service.update(id, new_data)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.update()")
            raise InternalServerError("algo salio mal")

    def delete(self, id: int) -> None:
        try:
            self.service.delete(id)
        except BaseHTTPException as ex:
            logger.error(
                f"Error al procesar request, status code {ex.status_code}: {ex.description}"
            )
            self.__handler_http_exception(ex)
        except Exception:
            logger.critical(f"Error no contemplado en {__name__}.delete()")
            raise InternalServerError("algo salio mal")
        
    def change_role(self, id, new_role: RoleEnum, user: DecodedJwt) -> UserResponse:
        try:
            return self.service.change_role(id, new_role, user)
        except BaseHTTPException as ex:
            self.__handler_http_exception(ex)
        except UniqueFieldException as ex:
            logger.error(str(ex))
            raise BadRequest("Error: campos duplicados")
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.create()" + str(ex))
            raise InternalServerError("Algo salio mal")
        

    def __handler_http_exception(self, ex: BaseHTTPException):
        if ex.status_code >= 500:
            logger.critical(
                f"Error en el servidor con status code {ex.status_code}: {ex.description}"
            )
        else:
            logger.error(f"Error {ex.status_code}: {ex.description}")

        raise ex
