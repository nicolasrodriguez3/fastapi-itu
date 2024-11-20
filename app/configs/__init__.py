from .settings import Settings
from .logging import config_logger
from .api_docs import api_description

settings = Settings()
config_logger(settings.DEBUG)