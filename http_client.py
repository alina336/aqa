import requests
from petstore.logging_config import logger
import allure


class HttpClient:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()  # Создание сессии для повторного использования соединений
        self.logger = logger

    def _request(self, method, endpoint, **kwargs):
        self.logger.info(f"Request: {method} {endpoint}.")
        if 'json' in kwargs:
            self.logger.info(f" Переданы параметры: {kwargs['json']}")
        try:
            response = self.session.request(method, endpoint, **kwargs)
            self.logger.info(f"Response: {response.status_code} - {response.text}.")
            return response
        except Exception as e:
            self.logger.error(f"ERROR: {str(e)}")
            raise

    @allure.step("Make GET request to {endpoint}")
    def get(self, endpoint):
        return self._request("GET", f"{self.url}{endpoint}")

    @allure.step("Make POST request to {endpoint}")
    def post(self, endpoint, json=None, data=None):
        return self._request("POST", f"{self.url}{endpoint}", json=json, data=data)

    @allure.step("Make PUT request to {endpoint}")
    def put(self, endpoint, json):
        return self._request("PUT", f"{self.url}{endpoint}", json=json)

    @allure.step("Make DELETE request to {endpoint}")
    def delete(self, endpoint):
        return self._request("DELETE", f"{self.url}{endpoint}")


"""
--------------------------------------------------------------------------------------------------
url = "https://petstore.swagger.io/v2"

response = requests.request("GET",f"{url}/pet/1")
#print(response.json())
new_pet = {
  "id": 49,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "bobby",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}

client = HttpClient(url)
#print(client.get("/pet/1").json())
print(client.post("/pet",new_pet).json())
print(client.get("/pet/49").json())
print(client.put("/pet",).json())
print(client.delete("/pet/49").json())
--------------------------------------------------------------------------------------------------
"""
