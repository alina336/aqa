import pytest
import time
from petstore.pet_client import PetClient


@pytest.mark.parametrize("input_data, expected_result", [({"id": 355},
                                                          {'id': 355, 'category': {"id": 0, "name": "category_unknown"},
                                                           "name": "name_unknown", "photoUrls": [], "tags": [],
                                                           "status": "status_unknown"}),
                                                         ({"id": 325, "category": {"id": 15, "name": "cats"}},
                                                          {"category": {'id': 15, "name": "cats"}, "id": 325,
                                                           "name": "name_unknown",
                                                           "photoUrls": [], "tags": [], "status": "status_unknown"}),
                                                         ({"id": 733, "category": {"id": 4, "name": "dogs"},
                                                           "name": "Jack", "tags": [{"id": 1, "name": "pet"}],
                                                           "status": "available", "photoUrls": ["url"]},
                                                          {"id": 733, "category": {"id": 4, "name": "dogs"},
                                                           "name": "Jack", "tags": [{"id": 1, "name": "pet"}],
                                                           "status": "available", "photoUrls": ["url"]}),
                                                         ],
                         ids=["test by id", "test by id and category", "test by all parameters"])
def test_add_pet_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.add_new_pet(**input_data)
    assert response.status_code == 200
    assert response.json() == expected_result


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
def test_update_pet_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.update_pet(**input_data)
    assert response.status_code == 200
    assert response.json() == expected_result
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("input_data, expected_result",
                         [("available", "available"), ("sold", "sold"), ("pending", "pending")],
                         ids=["test find pet by status: available", "test find pet by status: sold",
                              "test find pet by status: pending"])
def test_find_pet_by_status_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.find_pet_by_status(input_data)
    assert response.status_code == 200
    response.json()[0]["status"] == expected_result
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("input_data, expected_result", [(355, 355)], ids=["test find pet by id"])
def test_find_pet_by_id_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.find_pet_by_id(input_data)
    assert response.status_code == 200
    assert response.json()["id"] == expected_result
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("input_data, expected_result", [(355, "355")], ids=["test update pet with form data by id"])
def test_update_pet_with_form_data_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.update_pet_with_form_data(input_data)
    assert response.status_code == 200
    assert response.json()["message"] == expected_result
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("input_data, expected_result", [(355, "355")], ids=["test delete pet by id"])
def test_delete_pet_positive(input_data, expected_result):
    pet_client = PetClient()
    response = pet_client.delete_pet(input_data)
    assert response.status_code == 200
    assert response.json()["message"] == expected_result
    assert response.headers["Content-Type"] == "application/json"


"""
Негативные тесты
"""


@pytest.mark.parametrize("input_data", [({"id": 325, "category": "cats"}),
                                        ({"id": 733, "category": {"id": 4, "name": "dogs"},
                                          "name": "Jack", "tags": {"id": 1, "name": "pet"},
                                          "status": "available", "photoUrls": ["url"]}), ],
                         ids=["test add pet by wrong category type", "test by all parameters"])
def test_add_pet_negative(input_data):
    pet_client = PetClient()
    with pytest.raises(ValueError):
        pet_client.add_new_pet(**input_data)


@pytest.mark.parametrize("input_data", [({"id": -1, "category": {"id": -1, "name": "category_unknown"},
                                          "name": "Abby", "photoUrls": [], "tags": [],
                                          "status": "status_unknown"}),
                                        ({"id": 355, "category": "",
                                          "name": "Abby", "photoUrls": [], "tags": [],
                                          "status": "status_unknown"}),
                                        ({"id": "355", "category": {"id": -1, "name": "category_unknown"},
                                          "name": "Abby", "photoUrls": [], "tags": [],
                                          "status": "status_unknown"})],
                         ids=["test update pet`s name with wrong id", "test update pet`s category with wrong type",
                              "test update pet`s info with wrong id type"])
def test_update_pet_negative(input_data):
    pet_client = PetClient()
    with pytest.raises(ValueError):
        pet_client.update_pet(**input_data)


@pytest.mark.parametrize("input_data", [-1, None, ""],
                         ids=["test find pet by id with negative number", "test find pet by None id",
                              "test find pet by empty id"])
def test_find_pet_by_id_negative(input_data):
    pet_client = PetClient()
    with pytest.raises(ValueError):
        pet_client.find_pet_by_id(input_data)


@pytest.mark.parametrize("input_data",
                         ["new", "", ([1, 2, "sold"])],
                         ids=["test find pet by non-existent status", "test find pet by empty status",
                              "test find pet by statuses list with int"])
def test_find_pet_by_status_negative(input_data):
    with pytest.raises(ValueError):
        pet_client = PetClient()
        pet_client.find_pet_by_status(input_data)

@pytest.mark.parametrize("input_data", ["", -1, None],
                         ids=["test delete pet by empty id", "test delete pet by id < 0", "test delete pet by None id"])
def test_delete_pet_negative(input_data):
    with pytest.raises(ValueError):
        pet_client = PetClient()
        pet_client.delete_pet(input_data)


@pytest.mark.parametrize("input_data", ["", -1, None],
                         ids=["test update pet with form data by empty id", "test update pet with form data by id < 0",
                              "test update pet with form data by None id"])
def test_update_pet_with_form_data_negative(input_data):
    with pytest.raises(ValueError):
        pet_client = PetClient()
        pet_client.delete_pet(input_data)


"""
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
