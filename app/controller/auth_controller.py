import logging

from app.services import UsersService
from app.schemas import RegisterUser, LoginUser, TokenResponse
from app.exceptions import BaseHTTPException, BadRequest, InternalServerError


logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self) -> None:
        self.user_service = UsersService()
        self.auth_service = None

    def register(self, new_user: RegisterUser):
        try:
            pass
        except BaseHTTPException as ex:
            self.__handler_http_exception(ex)
        except Exception as ex:
            logger.critical(f"Error no contemplado en {__name__}.register(): {str(ex)}")
            raise InternalServerError("Error en register")

    def login(self, credentials: LoginUser):
        try:
            pass
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
