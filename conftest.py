import logging
from datetime import datetime
import pytest
from petstore.logging_config import setup_logging
from petstore.pet_client import PetClient


def pytest_configure(config):
    setup_logging()


@pytest.fixture(scope="module")
def pet_client():
    pet_client = PetClient()
    return pet_client


@pytest.fixture(scope="session", autouse=True)
def prepare_test_environment():
    print("Подготовка тестовых данных.")
    yield
    print("Удаление тестовых данных.")


@pytest.fixture(scope="session", autouse=True)
def log_session_setup():
    logger = logging.getLogger("conftest")
    logger.info("=" * 60)
    logger.info("НАЧАЛО СЕССИИ")
    yield
    logger.info("ЗАВЕРШЕНИЕ СЕССИИ")
    logger.info("=" * 60)

@pytest.fixture(autouse=True)
def log_test(request):
    test_name = request.node.name
    logger = logging.getLogger(test_name)
    start_time = datetime.now()
    logger.info(f"НАЧАЛО ТЕСТА {test_name}")
    yield
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"ЗАВЕРШЕНИЕ ТЕСТА: {test_name} | Время: {duration:.2f} сек")


