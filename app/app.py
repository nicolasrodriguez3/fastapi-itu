from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router
from .database import database_connection, create_table
from .middlewares import RequestLoggingMiddleware, JWTMiddleware
from .configs import api_description


@asynccontextmanager
async def lifespan(app: FastAPI):
    # if database_connection.connect():
    #     create_table()
    database_connection.connect()
    yield
    database_connection.disconnect()


app = FastAPI(
    lifespan=lifespan,
    **api_description,
)
app.include_router(router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(JWTMiddleware)