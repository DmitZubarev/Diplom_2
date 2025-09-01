import pytest
import allure

from resources.builders import user as u
from resources.steps.user import User


@allure.title("Создать пользователя")
@pytest.fixture
def new_user():
    payload = u.user_create()
    user = User(payload["email"], payload["password"], payload["name"])
    resp = user.user_create().json()

    for key in ("accessToken", "refreshToken"):
        payload[key] = resp[key]

    yield payload

    if resp:
        user.user_delete(payload["accessToken"])
