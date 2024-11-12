from app.configs import settings
from .db_connection import DBConnection


database_connection = DBConnection(settings.DB_CONN)