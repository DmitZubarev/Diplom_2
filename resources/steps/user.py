import allure

from helpers.api_client import HttpClient
from resources.builders import user as u
import resources.constants.endpoints as ep


class User:
    def __init__(self):
        self.client = HttpClient()

    @allure.step("Создаем пользователя")
    def user_create(self, email=None, password=None, name=None, generate=True):
        payload = u.user_create(
            email,
            password,
            name,
            generate
        )
        return self.client.post(endpoint=ep.REGISTER, json=payload)

    @allure.step("Авторизуемся пользователем")
    def user_login(self, email=None, password=None, generate=True):
        payload = u.user_login(
            email,
            password,
            generate
        )
        return self.client.post(endpoint=ep.LOGIN, json=payload)

    @allure.step("Изменяем данные пользователя")
    def user_update(self, email=None, password=None, name=None, generate=True, token=None):
        headers = u.user_auth(token)
        payload = u.user_create(
            email,
            password,
            name,
            generate
        )
        return self.client.patch(endpoint=ep.USER, json=payload, headers=headers)

    @allure.step("Удаляем пользователя")
    def user_delete(self, token=None):
        headers = u.user_auth(token)
        return self.client.delete(endpoint=ep.USER, headers=headers)
