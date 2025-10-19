import logging
from cgitb import handler
from datetime import datetime


def setup_logging():
    """Настройка логгера"""

    logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s',
                        filename=f'log{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log', filemode='w')
