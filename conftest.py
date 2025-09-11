import pytest
import allure

from resources.builders import user as u
from resources.builders import order as o
from resources.steps.user import User
from resources.steps.order import Order
from resources.steps.ingredients import Ingredients


@allure.title("Создать нового пользователя")
@pytest.fixture(scope="class")
def new_user():
    payload = u.user_create()
    resp = User().user_create(payload["email"], payload["password"], payload["name"]).json()

    for key in ("accessToken", "refreshToken"):
        payload[key] = resp[key]

    yield payload

    if resp:
        User().user_delete(payload["accessToken"])

@allure.title("Создать новый заказ")
@pytest.fixture(scope="class")
def new_order(new_user):
    ingredients = Ingredients().ingredients_get_list()
    payload = o.order_create(ingredients)
    resp = Order().order_create(ingredients, token=new_user["accessToken"], autofill=False).json()

    for key in ("_id", "number"):
        payload[key] = resp["order"][key]

    return payload
