import os
import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger(debug_level: bool):
    logger = logging.getLogger()
    if logger.hasHandlers():  # Evita agregar múltiples handlers.
        return
    
    LOGS_PATH = "./logs"
    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)

    log_filename = LOGS_PATH + "/app.log"
    logger.setLevel(logging.DEBUG if debug_level else logging.INFO)

    handler = TimedRotatingFileHandler(
        log_filename,
        when="midnight",
        backupCount=10,
        interval=1,
    )
    handler.suffix = "%Y%m%d"
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    # Configurar el logger del módulo watchfiles para ignorar logs de nivel INFO
    watchfiles_logger = logging.getLogger("watchfiles")
    watchfiles_logger.setLevel(logging.WARNING)  # Solo muestra WARNING o superior
