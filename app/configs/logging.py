import logging

def config_logger(debug_level: bool):
    LOGS_PATH = "./logs"
    
    log_filename = LOGS_PATH + "/app.log"
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug_level else logging.INFO)