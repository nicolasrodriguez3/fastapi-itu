from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware import Middleware

from .api import router
from .database import database_connection, create_table
from .middlewares import RequestLoggingMiddleware, JWTMiddleware

api_middlewares = [
    Middleware(RequestLoggingMiddleware),
    Middleware(JWTMiddleware),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # if database_connection.connect():
    #     create_table()
    database_connection.connect()
    yield
    database_connection.disconnect()


app = FastAPI(lifespan=lifespan, middleware=api_middlewares)
app.include_router(router)


# @app.on_event("startup")
# async def startup_event():
#     database_connection.connect()
    

# @app.on_event("shutdown")
# async def shutdown_event():
#     database_connection.disconnect()
    

    