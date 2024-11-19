import logging

from app.services import UsersService, AuthService
from app.schemas import RegisterUser, LoginUser, TokenResponse
from app.exceptions import (
    BaseHTTPException,
    BadRequest,
    InternalServerError,
    UniqueFieldException,
)


logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self) -> None:
        self.user_service = UsersService()
        self.auth_service = AuthService()

    def register(self, new_user: RegisterUser) -> TokenResponse:
        try:
            return self.auth_service.register(new_user)
        except BaseHTTPException as ex:
            self.__handler_http_exception(ex)
        except UniqueFieldException as ex:
            logger.error(str(ex))
            raise BadRequest("Error: campos duplicados")
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.register(): {str(ex)}")
            raise InternalServerError("Error en register")

    def login(self, credentials: LoginUser) -> TokenResponse:
        try:
            return self.auth_service.login(credentials)
        except BaseHTTPException as ex:
            self.__handler_http_exception(ex)
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.login(): {str(ex)}")
            raise InternalServerError("Error en login")

    def __handler_http_exception(self, ex: BaseHTTPException):
        if ex.status_code >= 500:
            logger.critical(
                f"Error en el servidor con status code {ex.status_code}: {ex.description}"
            )
        else:
            logger.error(f"Error {ex.status_code}: {ex.description}")

        raise ex
