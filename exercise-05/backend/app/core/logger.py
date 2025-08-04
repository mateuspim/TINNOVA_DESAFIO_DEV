import logging

def get_logger(name="app"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler("app.log")
        file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
    return logger

logger = get_logger()