from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import router
from .database import database_connection, create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    # if database_connection.connect():
        # create_table()
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
    

    