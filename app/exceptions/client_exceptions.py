from .base_http_exception import BaseHTTPException


class BadRequest(BaseHTTPException):
    description: str = 'Algo está mal con el request enviado por el cliente.'
    status_code = 400


class NotFound(BaseHTTPException):
    description: str = 'Recurso no encontrado'
    status_code = 404