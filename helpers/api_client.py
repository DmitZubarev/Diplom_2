import requests


BASE_URL = "https://stellarburgers.nomoreparties.site"

class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        return self.session.get(f"{BASE_URL}{endpoint}", params=params, headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return self.session.post(f"{BASE_URL}{endpoint}", json=json, headers=headers)

    def patch(self, endpoint, params=None, json=None, headers=None):
        return self.session.patch(f"{BASE_URL}{endpoint}", params=params, json=json, headers=headers)

    def delete(self, endpoint, json=None, headers=None):
        return self.session.delete(f"{BASE_URL}{endpoint}", json=json, headers=headers)
