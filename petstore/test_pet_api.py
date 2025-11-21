import time
import allure
import pytest
import requests
from deepdiff import DeepDiff
from petstore.data_generator import PetDataGenerator
import responses

"""Тесты с моками"""


@responses.activate
@allure.title("Mock-тест получения питомца по id")
def test_mock_find_pet_by_id(pet_client):
    responses.add(method=responses.GET, url="https://petstore.swagger.io/v2/pet/9989", json={"id": 9989, "name": "Rex"})
    pet = pet_client.find_pet_by_id(9989)
    assert pet.name == "Rex"


@responses.activate
@allure.title("Mock-тест удаления питомца по id")
def test_mock_delete_pet(pet_client):
    random_id = PetDataGenerator.id_generator()
    responses.add(method=responses.DELETE, url=f"https://petstore.swagger.io/v2/pet/{random_id}",
                  json={"code": 200, "type": "unknown", "message": str(random_id)})
    pet = pet_client.delete_pet(id=random_id)
    assert pet.message == str(random_id)
    assert pet.code == 200


@responses.activate
@allure.title("Mock-тест обновления питомца: id, status, tags")
def test_mock_update_pet(pet_client):
    random_pet = PetDataGenerator.generate_pet(only_specified=True, id=PetDataGenerator.id_generator(),
                                               status=PetDataGenerator.status_generator(),
                                               tags=PetDataGenerator.tags_generator())
    responses.add(method=responses.PUT, url="https://petstore.swagger.io/v2/pet",
                  json=random_pet)
    pet = pet_client.update_pet(**random_pet)
    print(pet.dict())
    assert pet.id == random_pet["id"]


"""Позитивные тесты"""


@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("create", "pet")
@allure.description("Тест проверяет создание питомца по id:"
                    "* создание питомца "
                    "* проверка успешности его создания")
@allure.title("Тест создания питомца по id")
def test_add_pet_positive(pet_client):
    input_data = PetDataGenerator.generate_full_pet()
    pet = pet_client.add_new_pet(**input_data)
    print(pet.dict())
    assert pet.id == input_data["id"]


@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("create", "pet")
@allure.description("Тест проверяет создание питомца по имени и статусу:"
                    "* создание питомца"
                    "* получение данных созданного питомца"
                    "* сравнивнение данных с помощью DeepDiff")
@allure.title("Тест создания питомца по имени и статусу")
def test_add_pet_exact_match(pet_client):
    input_data = PetDataGenerator.generate_pet(name="Rex", status="available")
    created_pet = pet_client.add_new_pet(**input_data)
    output_data = created_pet.dict()

    diff = DeepDiff(input_data, output_data, ignore_order=True)
    print(diff)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("update", "pet")
@allure.description("Тест проверяет изменение статуса питомца по его id:"
                    "* обновление статуса питомца"
                    "* получение данных обновленного питомца"
                    "* сравнивнение данных с помощью DeepDiff")
@allure.title("Тест обновления статуса питомца по id")
def test_update_pet_positive(pet_client):
    input_data = PetDataGenerator.generate_pet()
    updated_pet = pet_client.update_pet(**input_data)
    output_data = updated_pet.dict()
    print(updated_pet.dict())
    diff = DeepDiff(input_data, output_data, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


@pytest.mark.parametrize("input_data",
                         [PetDataGenerator.status_generator()],
                         ids=["test find pet by status"])
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("find", "pet")
@allure.description("Тест проверяет получение информации о питомце по его статусу:"
                    "* получение данных о питомце"
                    "* сравнивнение данных полученного статуса с переданным")
@allure.title("Тест создания питомца по name и status")
def test_find_pet_by_status_positive(input_data, pet_client):
    pets = pet_client.find_pet_by_status(input_data)
    assert pets[0].status == input_data


@pytest.mark.parametrize("input_data", [PetDataGenerator.id_generator()], ids=["test find pet by id"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("get", "pet")
@allure.description("Тест проверяет поиск питомца по id:"
                    "* создание питомца по id"
                    "* выполнение поиска питомца по id"
                    "* проверка успешности поиска питомца")
@allure.title("Тест поиска питомца по id")
def test_find_pet_by_id_positive(input_data, pet_client):
    pet_client.add_new_pet(id=input_data)
    time.sleep(10)
    pet = pet_client.find_pet_by_id(input_data)
    assert pet.id == input_data


@allure.severity(allure.severity_level.NORMAL)
@allure.tag("update", "pet")
@allure.description("Тест проверяет обновление информации о питомце данными по умолчанию:"
                    "* создание питомца по id"
                    "* обновление данных о питомце данными по умолчанию"
                    "* проверка успешности обновления данных о питомце")
@allure.title("Тест обновление информации о питомце данными по умолчанию")
def test_update_pet_with_form_data_positive(pet_client):
    rand_id = PetDataGenerator.id_generator()
    pet_client.add_new_pet(id=rand_id)
    time.sleep(15)
    pet = pet_client.update_pet_with_form_data(pet_id=rand_id, name="Buddy", status="sold")
    assert pet.message == str(rand_id)


@pytest.mark.parametrize("input_data", [PetDataGenerator.id_generator()], ids=["test delete pet by id"])
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("delete", "pet")
@allure.description("Тест проверяет удаление питомца по id:"
                    "* создание питомца по id"
                    "* удаление питомца по id"
                    "* проверка успешности удаления питомца")
@allure.title("Тест удаления питомца по id")
def test_delete_pet_positive(input_data, pet_client):
    pet_client.add_new_pet(id=input_data)
    time.sleep(5)
    pet = pet_client.delete_pet(input_data)
    assert pet.message == str(input_data)


"""Негативные тесты"""


@pytest.mark.parametrize("input_data", [({"id": 325, "category": "cats"}),
                                        ({"id": 733, "category": {"id": 4, "name": "dogs"},
                                          "name": "Jack", "tags": {"id": 1, "name": "pet"},
                                          "status": "available", "photoUrls": ["url"]}), ],
                         ids=["test add pet by wrong category type", "test by all parameters"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("create", "pet", "negative")
@allure.description("Тест проверяет создание питомца с некорректными данными:")
@allure.title("Негативный тест добавления питомца с некорректными данными.")
def test_add_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.add_new_pet(**input_data)


@pytest.mark.parametrize("input_data", [({"id": "id"}),
                                        ({"id": 355, "category": ""}),
                                        ({"id": "355", "tags": ""})],
                         ids=["test update pet`s name with wrong id type", "test update pet`s category with wrong type",
                              "test update pet`s info with wrong tags type"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("update", "pet", "negative")
@allure.description("Тест проверяет обновление питомца некорректными данными:")
@allure.title("Негативный тест обновления питомца некорректными данными.")
def test_update_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.update_pet(**input_data)


@pytest.mark.parametrize("input_data", [-1, None, ""],
                         ids=["test find pet by id with negative number", "test find pet by None id",
                              "test find pet by empty id"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("find", "pet", "negative")
@allure.description("Тест проверяет получение данных о питомце по некорректному id:")
@allure.title("Негативный тест получения данных о питомце по некорректному id.")
def test_find_pet_by_id_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.find_pet_by_id(input_data)


@pytest.mark.parametrize("input_data",
                         [None, "error", [1, 2, "sold"]],
                         ids=["test find pet by non-existent status", "test find pet by empty status",
                              "test find pet by statuses list with int"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("find", "pet", "negative")
@allure.description("Тест проверяет получение данных о питомце по некорректному статусу:")
@allure.title("Негативный тест получения данных о питомце по некорректному статусу.")
def test_find_pet_by_status_negative(input_data, pet_client):
    pets = pet_client.find_pet_by_status(input_data)
    assert pets == []


@pytest.mark.parametrize("input_data", [PetDataGenerator.invalid_id_generator()], ids=["test find pet by invalid_id"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("delete", "pet", "negative")
@allure.description("Тест проверяет удаление данных о питомце по некорректному id:")
@allure.title("Негативный тест удаления данных о питомце по некорректному id.")
def test_delete_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.delete_pet(input_data)


@pytest.mark.parametrize("input_data", [PetDataGenerator.invalid_id_generator()],
                         ids=["test update pet with form data by invalid_id"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("update", "pet", "negative")
@allure.description("Тест проверяет удаление данных о питомце по некорректному id:")
@allure.title("Негативный тест обновления данных о питомце по некорректному id.")
def test_update_pet_with_form_data_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.update_pet_with_form_data(input_data)


"""
fake = Faker()
first_name=fake.first_name()
pet_id=random.randint(2,1000)
status = random.choice(["available", "sold", "pending"])
photo_urls= [fake.image_url() for i in range(0)]
---------------------------------------------------------------------------------------------------
def test_add_pet_only_id():
    pet_client = PetClient()
    expected_result = {'category': {'id': 0, 'name': 'unknown'}, 'id': 355, 'photoUrls': [], 'tags': []}
    response = pet_client.add_new_pet(id=355)
    assert response.status_code == 200
    assert response.json() == expected_result


def test_add_pet_id_and_category():
    pet_client = PetClient()
    expected_result = {'category': {'id': 344, 'name': 'Liza'}, 'id': 355, 'photoUrls': [], 'tags': []}
    response = pet_client.add_new_pet(id=355, category={'id': 344, 'name': 'Liza'})
    assert response.status_code == 200
    assert response.json() == expected_result
---------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("input_data, expected_result", [({'id': 355, "category": {"id": 0, "name": "category_unknown"},
                                                           "name": "Abby", "photoUrls": [], "tags": [],
                                                           "status": "status_unknown"},
                                                          {'id': 355, "category": {"id": 0, "name": "category_unknown"},
                                                           "name": "Abby", "photoUrls": [], "tags": [],
                                                           "status": "status_unknown"}),
                                                         ({'id': 355, "category": {"id": 17, "name": "lemur"},
                                                           "name": "Abby", "photoUrls": [], "tags": [],
                                                           "status": "status_unknown"},
                                                          {'id': 355, "category": {"id": 17, "name": "lemur"},
                                                           "name": "Abby", "photoUrls": [], "tags": [],
                                                           "status": "status_unknown"}
                                                          ),
                                                         ({'id': 355, "category": {"id": 17, "name": "lemur"},
                                                           "name": "Abby", "photoUrls": ["new_url"], "tags": [],
                                                           "status": "sold"},
                                                          {'id': 355, "category": {"id": 17, "name": "lemur"},
                                                           "name": "Abby", "photoUrls": ["new_url"], "tags": [],
                                                           "status": "sold"}
                                                          )],
                         ids=["test update pet`s name", "test update pet`s category id and name",
                              "test update pet`s status and photoUrls"])

def test_update_pet_positive(input_data, expected_result, pet_client):
    pet_client.add_new_pet(id=input_data["id"])
    
    time.sleep(5)
    pet = pet_client.update_pet(**input_data)
    assert pet.dict() == expected_result
    print()
"""
