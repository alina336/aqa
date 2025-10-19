from deepdiff import DeepDiff
from pet_data_generator import PetDataGenerator

def test_add_pet_exact_match(pet_client):
    # Самый базовый вариант с переопределением нужных полей)

    input_data = PetDataGenerator.generate_pet(name="Rex", status="available")
    created_pet = pet_client.add_new_pet(**input_data)
    output_data = created_pet.dict()

    diff = DeepDiff(input_data, output_data, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"

def test_add_pet_ignore_extra_fields(pet_client):
    input_data = PetDataGenerator.generate_pet()
    created_pet = pet_client.add_new_pet(**input_data)
    output_data = created_pet.dict()

    # Оставляем только поля, которые есть в input_data
    filtered_output = {k: v for k, v in output_data.items() if k in input_data}

    diff = DeepDiff(input_data, filtered_output, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"

def test_add_pet_partial_override(pet_client):
    input_data = PetDataGenerator.generate_pet(name="Luna", status="sold")
    created_pet = pet_client.add_new_pet(**input_data)
    output_data = created_pet.dict()

    # Сравниваем только важные поля, игнорируя лишние
    important_fields = ["id", "name", "status", "category"]
    filtered_output = {k: output_data[k] for k in important_fields}
    filtered_input = {k: input_data[k] for k in important_fields}

    diff = DeepDiff(filtered_input, filtered_output, ignore_order=True)
    assert diff == {}, f"Поля не совпадают:\n{diff}"


# Если очень хотим параметризацию :)

@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_find_pet_by_status(pet_client, status):
    pet_data = PetDataGenerator.generate_pet(status=status)
    pet_client.add_new_pet(**pet_data)

    found_pets = pet_client.find_pet_by_status(status)
    output_data = [p.dict() for p in found_pets]

    # DeepDiff на первом найденном питомце
    from deepdiff import DeepDiff
    diff = DeepDiff(pet_data, output_data[0], ignore_order=True)
    assert diff == {}
