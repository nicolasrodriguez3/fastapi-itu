from .settings import Settings
from .logging import config_logger

settings = Settings()
config_logger(settings.DEBUG)