import pytest
import allure

from resources.steps.user import User
from resources.constants import status_codes, error_messages
from helpers.data_generator import generate_credentials
from helpers.schema_validator import validate_schema


@allure.suite("Проверки метода создания пользователя")
class TestUserCreate:

    @allure.title("Создание уникального пользователя")
    def test_user_create_success(self):
        user = User()
        resp = user.user_create()
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "user_create")

        user.user_delete(resp.json()["accessToken"])

    @allure.title("Создание не уникального пользователя")
    def test_user_create_with_existing_login(self, new_user):
        resp = User(new_user["email"], new_user["password"], new_user["name"]).user_create()
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.USER_EXISTS
        validate_schema(resp.json(), "error_message")

    @allure.title("Создание пользователя без передачи обязательных полей")
    @pytest.mark.parametrize("email, password, name", [(None, generate_credentials()[1], generate_credentials()[2]),
                                                       (generate_credentials()[0], None, generate_credentials()[2]),
                                                       (generate_credentials()[0], generate_credentials()[1], None)],
                             ids=["Отсутствует email", "Отсутствует password", "Отсутствует name"])
    def test_user_create_with_empty_fields(self, email, password, name):
        resp = User(email, password, name, generate=False).user_create()
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.CREDENTIAL_MISSING
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода авторизации пользователя")
class TestUserLogin:

    @allure.title("Авторизация существующего пользователя")
    def test_user_login_success(self, new_user):
        resp = User(new_user["email"], new_user["password"]).user_login()
        assert resp.status_code == status_codes.CODE_OK
        assert resp.json()["user"]["email"] == new_user["email"]
        validate_schema(resp.json(), "user_login")

    @allure.title("Авторизация пользователя с некорректными данными")
    @pytest.mark.parametrize("invalid", [({"email": generate_credentials()[0]}),
                                         ({"password": generate_credentials()[1]}),
                                         ({"email": generate_credentials()[0], "password": generate_credentials()[1]})],
                             ids=["Неверный email", "Неверный password", "Неверные email и password"])
    def test_user_login_wrong_creds(self, new_user, invalid):
        credentials = {**new_user, **invalid}
        resp = User(credentials["email"], credentials["password"]).user_login()
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.CREDENTIAL_INCORRECT
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода редактирования пользователя")
class TestUserUpdate:

    @allure.title("Редактирование авторизованного пользователя")
    def test_user_update_success(self, new_user):
        resp = User().user_update(new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_OK
        assert resp.json()["user"]["email"] != new_user["email"]
        validate_schema(resp.json(), "user_edit")

    @allure.title("Редактирование неавторизованного пользователя")
    def test_user_update_without_auth(self, new_user):
        resp = User().user_update()
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.UNAUTHORIZED
        validate_schema(resp.json(), "error_message")
