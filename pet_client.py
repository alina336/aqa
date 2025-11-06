from petstore.http_client import HttpClient
import allure
from petstore.models import Pet, PetMessage


class PetClient(HttpClient):

    def __init__(self):
        super().__init__(url="https://petstore.swagger.io/v2")
        self.base_endpoint = "/pet"

    @allure.step("Add new pet")
    def add_new_pet(self, **pet_data):
        response = self.post(self.base_endpoint, json=pet_data)
        response.raise_for_status()
        return Pet(**response.json())

    @allure.step("Update existing pet")
    def update_pet(self, **pet_data):
        response = self.put(self.base_endpoint, json=pet_data)
        response.raise_for_status()
        return Pet(**response.json())

    @allure.step("Get existing pets by status")
    def find_pet_by_status(self, status):
        if isinstance(status, list):
            status_params = [f"status={s}" for s in status]
            statuses = "&".join(status_params)
        else:
            statuses = f"status={status}"
        endpoint = f"{self.base_endpoint}/findByStatus?{statuses}"
        response = self.get(endpoint)
        response.raise_for_status()
        return [Pet(**pet_data) for pet_data in response.json()]

    @allure.step("Get existing pet by id")
    def find_pet_by_id(self, id=0):
        endpoint = f"{self.base_endpoint}/{id}"
        response = self.get(endpoint)
        response.raise_for_status()
        return Pet(**response.json())

    @allure.step("Update existing pet with form data")
    def update_pet_with_form_data(self, id):
        endpoint = f"{self.base_endpoint}/{id}"
        response = self.post(endpoint)
        response.raise_for_status()
        return PetMessage(**response.json())

    @allure.step("Delete existing pet")
    def delete_pet(self, id):
        endpoint = f"{self.base_endpoint}/{id}"
        response = self.delete(endpoint)
        response.raise_for_status()
        return PetMessage(**response.json())


"""
    def add_new_pet(self, **pet_data):
        data = {}
        pet_id = pet_data.get("id", 1)
        if not isinstance(pet_id, int) or pet_id < 0:
            raise ValueError("Значение ID должно быть целым положительным числом.")
        data["id"] = pet_id
        category = pet_data.get("category", {"id": 0, "name": "category_unknown"})
        if not isinstance(category, dict) or list(category.keys()) != ["id", "name"]:
            raise ValueError("Категория должна быть словарем с ключами id и name.")
        data["category"] = category
        data["name"] = pet_data.get("name", "name_unknown")
        data["photoUrls"] = pet_data.get("photoUrls", [])
        tags = pet_data.get("tags", [])
        if not isinstance(tags, list):
            raise ValueError("Теги должны быть списком")
        data["tags"] = tags
        data["status"] = pet_data.get("status", "status_unknown")
        return self.post(self.base_endpoint, json=data)
        
    def find_pet_by_id(self, id=0):
        endpoint = f"{self.base_endpoint}/{id}"
        if not isinstance(id, int) or id < 0:
            raise ValueError("Значение ID должно быть целым положительным числом.")
        return self.get(endpoint)

   def update_pet(self, **pet_data):
        data = {}
        pet_id = pet_data.get("id")
        if not isinstance(pet_id, int) or pet_id < 0:
            raise ValueError("Значение ID должно быть целым положительным числом.")
        data["id"] = pet_id
        category = pet_data.get("category", {"id": 0, "name": "category_unknown"})
        if not isinstance(category, dict) or list(category.keys()) != ["id", "name"]:
            raise ValueError("Категория должна быть словарем с ключами id и name.")
        data["category"] = category
        data["name"] = pet_data.get("name", "name_unknown")
        photo_urls = pet_data.get("photoUrls", [])
        if not isinstance(photo_urls, list) or list(category.keys()) != ["id", "name"]:
            raise ValueError("Необходимо ввести список строк со ссылками на фото.")
        data["photoUrls"] = photo_urls
        tags = pet_data.get("tags", [])
        data["tags"] = tags
        data["status"] = pet_data.get("status", "status_unknown")
        return self.put(self.base_endpoint, json=data)
        
   def update_pet_with_form_data(self, id):
    endpoint = f"{self.base_endpoint}/{id}"
    if not isinstance(id, int) or id < 0:
        raise ValueError("Значение ID должно быть целым положительным числом.")
    return self.post(endpoint)     
    
    
    def delete_pet(self, id):
        endpoint = f"{self.base_endpoint}/{id}"
        if not isinstance(id, int) or id < 0:
            raise ValueError("Значение ID должно быть целым положительным числом.")
        return self.delete(endpoint)
        def find_pet_by_status(self, status):
        endpoint = f"{self.base_endpoint}/findByStatus?status={status}"
        if not isinstance(status, list) and len(status) < 1:
            raise ValueError("Значение status должно быть списком строк.")
        for i in status:
            if not isinstance(i, str) or i not in ["available", "pending", "sold"]:
                raise ValueError(
                    "Значение status должно быть списком строк. Возможные значения: available, pending, sold.")
        return self.get(endpoint)
---------------------------------------------------------------------------------------------------
pet_client=PetClient()
print(pet_client.add_new_pet(id=355).json())
time.sleep(3)
print(pet_client.find_pet_by_id(355).json())
print(pet_client.find_pet_by_status("available").json())
print(pet_client.update_pet(update_pet_data).json())
print(pet_client.find_pet_by_id(45).json())
print(pet_client.find_pet_by_status("sold").json())
print(pet_client.update_pet_with_form_data(45).json())
print(pet_client.find_pet_by_id(45).json())
print(pet_client.delete_pet(45).json())
print(pet_client.find_pet_by_id(45).json())

-------------------------------------------------------------------------------------------------------
"""
