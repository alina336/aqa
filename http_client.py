import requests

url = "https://petstore.swagger.io/v2"


class HttpClient:
    def __init__(self):
        self.url = url
        self.session = requests.Session()

    def _request(self, method, endpoint, json=None):
        return self.session.request(method, endpoint, json=json)

    def get(self, endpoint):
        return self._request("GET", f"{url}{endpoint}")

    def post(self, endpoint, json=None):
        return self._request("POST", f"{url}{endpoint}", json=json)

    def put(self, endpoint, json):
        return self._request("PUT", f"{url}{endpoint}", json=json)

    def delete(self, endpoint):
        return self._request("DELETE", f"{url}{endpoint}")


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
