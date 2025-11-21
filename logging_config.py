import logging
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)-8s] %(name)-15s: %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    # Обработчик для файла
    file_handler = logging.FileHandler(filename="logs/tests.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Настройка главного логгера
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    return logger