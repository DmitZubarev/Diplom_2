import allure

from resources.steps.order import Order
from resources.steps.ingredients import Ingredients
from resources.constants import status_codes, error_messages
from helpers.schema_validator import validate_schema


@allure.suite("Проверки метода создания заказа")
class TestOrderCreate:

    @allure.title("Создание заказа пользователем")
    def test_order_create_success(self, new_user):
        ingredients = Ingredients().ingredients_get_list()
        resp = Order().order_create(ingredients, token=new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_OK
        assert resp.json()["order"]["owner"]["email"] == new_user["email"]
        validate_schema(resp.json(), "order_create_authorized")

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_order_create_without_auth(self):
        ingredients = Ingredients().ingredients_get_list()
        resp = Order().order_create(ingredients)
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "order_create_unauthorized")

    @allure.title("Создание заказа без ингредиентов")
    def test_order_create_without_ingredients(self, new_user):
        resp = Order().order_create(token=new_user["accessToken"], generate=False)
        assert resp.status_code == status_codes.CODE_BAD_REQUEST
        assert resp.json()["message"] == error_messages.INGREDIENTS_MISSING
        validate_schema(resp.json(), "error_message")

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_create_wrong_ingredient_hash(self, new_user):
        resp = Order().order_create(token=new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_INTERNAL_SERVER_ERROR


@allure.suite("Проверки метода получения заказа")
class TestOrderGet:

    @allure.title("Получение списка заказов пользователя")
    def test_order_get_success(self, new_user, new_order):
        resp = Order().order_get(token=new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_OK
        assert new_order["_id"] in [order["_id"] for order in resp.json()["orders"]]
        validate_schema(resp.json(), "order_get_authorized")

    @allure.title("Получение списка заказов неавторизованного пользователя")
    def test_order_get_without_auth(self, new_user, new_order):
        resp = Order().order_get()
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.UNAUTHORIZED
        validate_schema(resp.json(), "error_message")
