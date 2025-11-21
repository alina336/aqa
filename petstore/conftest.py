from datetime import datetime
import pytest
from utils.logging_config import logger
from petstore.pet_client import PetClient
from petstore.database_client import DBClient
from petstore.pet_repository import PetRepository


@pytest.fixture(scope="module")
def pet_client():
    pet_client = PetClient()
    return pet_client


@pytest.fixture(scope="session", autouse=True)
def prepare_test_environment():
    logger.info("Подготовка тестовых данных.")
    yield
    logger.info("Удаление тестовых данных.")


@pytest.fixture(scope="session", autouse=True)
def log_session_setup():
    logger.info("=" * 60)
    logger.info("НАЧАЛО СЕССИИ")
    yield
    logger.info("ЗАВЕРШЕНИЕ СЕССИИ")
    logger.info("=" * 60)


@pytest.fixture(autouse=True)
def log_test(request):
    test_name = request.node.name
    start_time = datetime.now()
    logger.info(f"НАЧАЛО ТЕСТА {test_name}")
    yield
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"ЗАВЕРШЕНИЕ ТЕСТА: {test_name} | Время: {duration:.2f} сек")


@pytest.fixture(scope="session")
def cursor():
    with DBClient(host="localhost",
                  port=5432,
                  database="mytestdb",
                  user="postgres",
                  password="PASSWORD") as db:
        yield db
    logger.info("Удаление клиента")

@pytest.fixture(scope="session")
def pet_repo(cursor):
    repo = PetRepository(cursor)
    yield repo