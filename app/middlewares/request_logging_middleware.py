import logging
import json
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("request_logger")

SENSITIVE_DATA_FIELDS = ["password"]


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Log the request details
        method = request.method
        url = str(request.url.path)
        client_ip: str = request.client.host
        query_params = dict(request.query_params)
        
         # Obtener el tipo de contenido
        content_type = request.headers.get("content-type", "")
        raw_body = await request.body()

        # Procesar el cuerpo según el tipo de contenido
        if "application/json" in content_type:
            try:
                body = json.loads(raw_body)
            except json.JSONDecodeError:
                body = {"error": "Invalid JSON"}
        elif "application/x-www-form-urlencoded" in content_type:
            body = dict((pair.split("=", 1) for pair in raw_body.decode().split("&")))
        else:
            body = raw_body.decode("utf-8")  # Procesar como texto simple

        # Ocultar datos sensibles
        body = self.__hide_sensitive_data(body)

        # Registrar el tiempo de inicio
        start_time = time.perf_counter()

        # Endpoint
        response = await call_next(request)

        # Calcular tiempo de ejecución
        execution_time = time.perf_counter() - start_time
        
        request_info = (
            f"{client_ip} - {method} {url} {query_params} - {response.status_code} - {execution_time:.2f}s"
        )
        if body:
            request_info += f"\n{str(body)}"

        logger.info(request_info)

        return response

    def __hide_sensitive_data(self, body):
        """
        Oculta los campos sensibles del cuerpo de la solicitud.
        """
        if not body:
            return body

        if isinstance(body, dict):  # Manejar solo si es un diccionario
            for field in SENSITIVE_DATA_FIELDS:
                if field in body:
                    body[field] = "********"
            return body

        # Si el cuerpo es una cadena o texto plano, no hacer nada
        return body