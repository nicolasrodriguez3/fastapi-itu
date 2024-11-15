from app.configs import settings
from .db_connection import DBConnection
from .models import BaseModel

database_connection = DBConnection(settings.DB_CONN)
def create_table() -> None:
    BaseModel.metadata.create_all(bind=database_connection.engine)