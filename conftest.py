import time
from data_generator import generator
from logging_config import setup_logging
import pytest
from petstore.pet_client import PetClient

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


@pytest.fixture
def random_fields():
    return {
        "id": generator.id_generator(),
        "category": {
            "id": generator.id_generator(),
            "name": generator.category_name_generator()
        },
        "name": generator.name_generator(),
        "photoUrls": generator.photo_url_generator(),
        "tags": [
            {
                "id": generator.id_generator(),
                "name": generator.tags_generator()
            }
        ],
        "status": generator.status_generator()
    }
