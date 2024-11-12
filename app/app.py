from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import router
from .database import database_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    database_connection.connect()
    yield
    database_connection.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


# @app.on_event("startup")
# async def startup_event():
#     database_connection.connect()
    

# @app.on_event("shutdown")
# async def shutdown_event():
#     database_connection.disconnect()
    

    