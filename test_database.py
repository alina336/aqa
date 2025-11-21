import allure
import requests
from deepdiff import DeepDiff
from petstore.data_generator import PetDataGenerator, DataMapper
import responses


@allure.title("Тест подключения к БД")
def test_db_connection(cursor):
    with allure.step(f"Тест текущего пользователя"):
        user = cursor.execute("SELECT current_user;")
        assert user[0][0] == "postgres"


@allure.title("Тест вывода количества пользователей БД")
def test_select_count_users(cursor):
    users_count = cursor.execute("SELECT COUNT(*) FROM users;")
    assert users_count[0][0] == 2


def test_add_new_pet_info_to_db(cursor, pet_client):
    input_data = PetDataGenerator.generate_full_pet()
    pet = pet_client.add_new_pet(**input_data)
    print(pet.dict())
    mapped_data = DataMapper.map_to_tables(input_data)
    print(f"MD: {mapped_data}, MD keys: {mapped_data.keys()}")
    print(f"InpD: {input_data}, InpD keys: {input_data.keys()}")
    cursor.insert_pet_data(mapped_data)
    inserted_data_pet = cursor.execute(f"SELECT * FROM pets where id = {mapped_data["pets"]["id"]}")[0]
    print(f"Inserted data: {inserted_data_pet}")
    assert input_data["id"] == inserted_data_pet[0]
    assert input_data["name"] == inserted_data_pet[1]
    assert input_data["status"] == inserted_data_pet[2]


def test_add_updated_pet_to_db(cursor, pet_client):
    input_data = PetDataGenerator.generate_pet(id=50, name=PetDataGenerator.name_generator(),
                                               status=PetDataGenerator.status_generator())
    pet = pet_client.update_pet(**input_data)
    print(pet.dict())
    mapped_data = DataMapper.map_to_tables(input_data)
    cursor.insert_pet_data(mapped_data)
    inserted_data_pet = cursor.execute(f"SELECT * FROM pets where id = {mapped_data["pets"]["id"]}")[0]
    inserted_data_category = cursor.execute(f"SELECT * FROM categories where pet_id = {mapped_data["pets"]["id"]}")[0]
    assert input_data["id"] == inserted_data_pet[0]
    assert input_data["name"] == inserted_data_pet[1]
    assert input_data["status"] == inserted_data_pet[2]
    assert input_data["category"]["id"] == inserted_data_category[0]
    assert input_data["category"]["name"] == inserted_data_category[1]


def test_add_found_pet_info_to_db(cursor, pet_client):
    # rand_id=PetDataGenerator.id_generator()
    # input_data = PetDataGenerator.generate_pet(only_specified=True, id=rand_id)
    # pet_client.add_new_pet(**input_data)
    pet = pet_client.find_pet_by_id(id=55)
    mapped_data = DataMapper.map_to_tables(pet.dict())
    cursor.insert_pet_data(mapped_data)
    inserted_data_pet = cursor.execute(f"SELECT * FROM pets where id = {mapped_data["pets"]["id"]}")[0]
    assert pet.id == inserted_data_pet[0]
    assert pet.name == inserted_data_pet[1]
    assert pet.status == inserted_data_pet[2]


def test_delete_pet_from_db(cursor):
    pet_id = 55
    cursor.execute(f"BEGIN;"
                   f"DELETE FROM photos WHERE pet_id = {pet_id};"
                   f"DELETE FROM tags WHERE pet_id = {pet_id};"
                   f"DELETE FROM categories WHERE pet_id = {pet_id};"
                   f"DELETE FROM pets WHERE id = {pet_id};"
                   f"COMMIT;")
    result = cursor.execute(f"SELECT * FROM pets where id = {pet_id}")
    assert result == []