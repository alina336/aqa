import time

import pytest
import requests
from faker import Faker
import random
from data_generator import PetDataGenerator


@pytest.mark.parametrize("input_data", [({"id": PetDataGenerator.id_generator()})])
def test_add_pet_by_id_positive(input_data, pet_client):
    # pet = generate_pet_data
    pet = pet_client.add_new_pet(**input_data)
    print(pet.dict())
    assert pet.id == input_data["id"]


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


@pytest.mark.parametrize("input_data",
                         [PetDataGenerator.status_generator()],
                         ids=["test find pet by status"])
def test_find_pet_by_status_positive(input_data, pet_client):
    pets = pet_client.find_pet_by_status(input_data)
    assert pets[0].status == input_data


@pytest.mark.parametrize("input_data", [PetDataGenerator.id_generator()], ids=["test find pet by id"])
def test_find_pet_by_id_positive(input_data, pet_client):
    pet_client.add_new_pet(id=input_data)
    time.sleep(10)
    pet = pet_client.find_pet_by_id(input_data)
    assert pet.id == input_data


@pytest.mark.parametrize("input_data", [PetDataGenerator.id_generator()], ids=["test update pet with form data by id"])
def test_update_pet_with_form_data_positive(input_data, pet_client):
    pet_client.add_new_pet(id=input_data)
    time.sleep(15)
    pet = pet_client.update_pet_with_form_data(input_data)
    assert pet.message == str(input_data)


@pytest.mark.parametrize("input_data", [PetDataGenerator.id_generator()], ids=["test delete pet by id"])
def test_delete_pet_positive(input_data, pet_client):
    pet_client.add_new_pet(id=input_data)
    time.sleep(5)
    pet = pet_client.delete_pet(input_data)
    assert pet.message == str(input_data)


"""
Негативные тесты
"""


@pytest.mark.parametrize("input_data", [({"id": 325, "category": "cats"}),
                                        ({"id": 733, "category": {"id": 4, "name": "dogs"},
                                          "name": "Jack", "tags": {"id": 1, "name": "pet"},
                                          "status": "available", "photoUrls": ["url"]}), ],
                         ids=["test add pet by wrong category type", "test by all parameters"])
def test_add_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.add_new_pet(**input_data)


@pytest.mark.parametrize("input_data", [({"id": "id"}),
                                        ({"id": 355, "category": ""}),
                                        ({"id": "355", "tags": ""})],
                         ids=["test update pet`s name with wrong id type", "test update pet`s category with wrong type",
                              "test update pet`s info with wrong tags type"])
def test_update_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.update_pet(**input_data)


@pytest.mark.parametrize("input_data", [-1, None, ""],
                         ids=["test find pet by id with negative number", "test find pet by None id",
                              "test find pet by empty id"])
def test_find_pet_by_id_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.find_pet_by_id(input_data)


@pytest.mark.parametrize("input_data",
                         [None, "error", [1, 2, "sold"]],
                         ids=["test find pet by non-existent status", "test find pet by empty status",
                              "test find pet by statuses list with int"])
def test_find_pet_by_status_negative(input_data, pet_client):
    pets = pet_client.find_pet_by_status(input_data)
    assert pets == []


@pytest.mark.parametrize("input_data", ["", -1, None],
                         ids=["test delete pet by empty id", "test delete pet by id < 0", "test delete pet by None id"])
def test_delete_pet_negative(input_data, pet_client):
    with pytest.raises(requests.exceptions.HTTPError):
        pet_client.delete_pet(input_data)


@pytest.mark.parametrize("input_data", ["", -1, None],
                         ids=["test update pet with form data by empty id", "test update pet with form data by id < 0",
                              "test update pet with form data by None id"])
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
"""
