import allure

from helpers.api_client import HttpClient
from resources.builders import user as u
import resources.constants.endpoints as ep


class User:

    def __init__(self, email=None, password=None, name=None, autofill=True):
        self.client = HttpClient()
        self.email = email
        self.password = password
        self.name = name
        self.autofill = autofill

    @allure.step("Создать пользователя")
    def user_create(self):
        payload = u.user_create(
            self.email,
            self.password,
            self.name,
            self.autofill
        )
        return self.client.post(endpoint=ep.REGISTER, json=payload)

    @allure.step("Авторизоваться пользователем")
    def user_login(self):
        payload = u.user_login(
            self.email,
            self.password
        )
        response = self.client.post(endpoint=ep.LOGIN, json=payload)
        return response

    @allure.step("Изменить данные пользователя")
    def user_update(self, auth=None):
        payload = u.user_create(
            self.email,
            self.password,
            self.name,
        )
        return self.client.patch(endpoint=ep.USER, json=payload, headers={"Authorization": auth})

    @allure.step("Удалить пользователя")
    def user_delete(self, auth=None):
        return self.client.delete(endpoint=ep.USER, headers={"Authorization": auth})
