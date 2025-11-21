import time

import allure
from deepdiff import DeepDiff
from petstore.data_generator import PetDataGenerator
from utils.logging_config import logger


@allure.title("Тест подключения к БД")
def test_db_connection(cursor):
    with allure.step(f"Тест текущего пользователя"):
        user = cursor.execute("SELECT current_user;")
        logger.info(user)
        assert user[0]['current_user'] == 'postgres'


@allure.title("Тест вывода количества пользователей БД")
def test_select_count_users(cursor):
    users_count = cursor.execute("SELECT COUNT(*) FROM users;")
    logger.info(users_count)
    assert users_count[0]['count'] == 2


def test_add_new_pet_info_to_db(pet_client, pet_repo):
    input_data = PetDataGenerator.generate_full_pet()
    pet = pet_client.add_new_pet(**input_data)
    logger.info(pet.dict())
    pet_repo.save_pet_to_db(pet.dict())
    logger.info(pet.dict())
    data_from_db = pet_repo.get_pet_from_db(pet.id)
    logger.info(f"{data_from_db}")
    diff = DeepDiff(pet.dict(), data_from_db, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


def test_add_updated_pet_to_db(pet_repo, pet_client):
    input_data = PetDataGenerator.generate_pet(id=50, name=PetDataGenerator.name_generator(),
                                               status=PetDataGenerator.status_generator())
    pet = pet_client.update_pet(**input_data)
    logger.info(pet.dict())
    pet_repo.save_pet_to_db(pet.dict())
    data_from_db = pet_repo.get_pet_from_db(pet.id)
    logger.info(f"{data_from_db}")
    diff = DeepDiff(pet.dict(), data_from_db, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


def test_add_found_pet_info_to_db(pet_repo, pet_client):
    rand_id = PetDataGenerator.id_generator()
    input_data = PetDataGenerator.generate_pet(only_specified=True, id=rand_id)
    pet_client.add_new_pet(**input_data)
    time.sleep(30)
    pet = pet_client.find_pet_by_id(id=rand_id)
    logger.info(pet.dict())
    pet_repo.save_pet_to_db(pet.dict())
    data_from_db = pet_repo.get_pet_from_db(pet.id)
    logger.info(data_from_db)
    diff = DeepDiff(pet.dict(), data_from_db, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


def test_delete_pet_from_db(pet_repo):
    pet_id = 50
    pet_repo.delete_pet_from_db(pet_id)
    result = pet_repo.get_pet_from_db(pet_id)
    assert result == {}