import allure

from helpers.api_client import HttpClient
from resources.builders import order as o
from resources.builders import user as u
import resources.constants.endpoints as ep


class Order:

    def __init__(self):
        self.client = HttpClient()

    @allure.step("Создать заказ")
    def order_create(self, ingredients: list[str]=None, token=None, amount=3, autofill=True):
        headers = u.user_auth(token)
        payload = o.order_create(
            ingredients,
            amount,
            autofill
        )
        return self.client.post(endpoint=ep.ORDERS, json=payload, headers=headers)

    @allure.step("Получить список заказов пользователя")
    def order_get(self, token=None):
        headers = u.user_auth(token)
        return self.client.get(endpoint=ep.ORDERS, headers=headers)
