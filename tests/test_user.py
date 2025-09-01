import pytest
import allure

from resources.steps.user import User
from resources.constants import status_codes, error_messages
from helpers.data_generator import generate_credentials
from helpers.schema_validator import validate_schema


@allure.suite("Проверки метода создания пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_user_success(self):
        user = User()
        resp = user.user_create()
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "user_create")

        user.user_delete(resp.json()["accessToken"])

    @allure.title("Создание не уникального пользователя")
    def test_create_user_with_existing_login(self, new_user):
        user = User(new_user["email"], new_user["password"], new_user["name"])
        resp = user.user_create()
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.USER_EXISTS
        validate_schema(resp.json(), "error_message")

    @allure.title("Создание пользователя без передачи обязательных полей")
    @pytest.mark.parametrize("email, password, name", [(None, generate_credentials()[1], generate_credentials()[2]),
                                                       (generate_credentials()[0], None, generate_credentials()[2]),
                                                       (generate_credentials()[0], generate_credentials()[1], None)],
                             ids=["Отсутствует email", "Отсутствует password", "Отсутствует name"])
    def test_create_user_with_empty_fields(self, email, password, name):
        user = User(email, password, name, autofill=False)
        resp = user.user_create()
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.FIELDS_MISSING
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода авторизации пользователя")
class TestLoginUser:

    @allure.title("Авторизация существующего пользователя")
    def test_login_user_success(self, new_user):
        user = User(new_user["email"], new_user["password"])
        resp = user.user_login()
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "user_login")

    @allure.title("Авторизация пользователя с некорректными данными")
    @pytest.mark.parametrize("invalid", [({"email": generate_credentials()[0]}),
                                         ({"password": generate_credentials()[1]}),
                                         ({"email": generate_credentials()[0], "password": generate_credentials()[1]})],
                             ids=["Неверный email", "Неверный password", "Неверные email и password"])
    def test_login_user_wrong_creds(self, new_user, invalid):
        credentials = {**new_user, **invalid}
        user = User(credentials["email"], credentials["password"])
        resp = user.user_login()
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.INCORRECT_CREDENTIAL
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода редактирования пользователя")
class TestUpdateUser:

    @allure.title("Редактирование авторизованного пользователя")
    def test_update_user_success(self, new_user):
        user = User()
        resp = user.user_update(new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "user_edit")

    @allure.title("Редактирование неавторизованного пользователя")
    def test_update_user_without_auth(self, new_user):
        user = User()
        resp = user.user_update()
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.UNAUTHORIZED
        validate_schema(resp.json(), "error_message")
