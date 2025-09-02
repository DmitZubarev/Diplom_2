import allure
import random

from helpers.api_client import HttpClient
import resources.constants.endpoints as ep


class Ingredients:

    def __init__(self):
        self.client = HttpClient()

    @allure.step("Получить данные об ингредиентах")
    def ingredients_get(self):
        return self.client.get(endpoint=ep.INGREDIENTS)

    @allure.step("Получить список случайных ингредиентов")
    def ingredients_get_list(self, amount=3):
        ingredients = []
        resp = self.ingredients_get().json()
        ids = [item["_id"] for item in resp["data"]]
        for i in range(amount):
            ingredients.append(random.choice(ids))
        return ingredients
