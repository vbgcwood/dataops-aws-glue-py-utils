# logging_utils.py
import logging


def setup_logger(
    name: str,
    level=logging.INFO,
    fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Creates and configures a dedicated logger.

    Parameters:
    - name (str): Name of the logger.
    - level (int): Logging level.
    - fmt (str): Logging format.

    Returns:
    - logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
