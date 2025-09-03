import pytest
import allure

from resources.steps.user import User
from resources.constants import status_codes, error_messages
from helpers.data_generator import generate_credentials as gen_creds
from helpers.schema_validator import validate_schema


@allure.suite("Проверки метода создания пользователя")
class TestUserCreate:

    @allure.title("Создание уникального пользователя")
    def test_user_create_success(self):
        resp = User().user_create(gen_creds()[0], gen_creds()[1], gen_creds()[2])
        assert resp.status_code == status_codes.CODE_OK
        validate_schema(resp.json(), "user_create")

        User().user_delete(resp.json()["accessToken"])

    @allure.title("Создание не уникального пользователя")
    def test_user_create_with_existing_login(self, new_user):
        resp = User().user_create(new_user["email"], new_user["password"], new_user["name"])
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.USER_EXISTS
        validate_schema(resp.json(), "error_message")

    @allure.title("Создание пользователя без передачи обязательных полей")
    @pytest.mark.parametrize("email, password, name", [(None, gen_creds()[1], gen_creds()[2]),
                                                       (gen_creds()[0], None, gen_creds()[2]),
                                                       (gen_creds()[0], gen_creds()[1], None)],
                             ids=["Отсутствует email", "Отсутствует password", "Отсутствует name"])
    def test_user_create_with_empty_fields(self, email, password, name):
        resp = User().user_create(email, password, name, generate=False)
        assert resp.status_code == status_codes.CODE_FORBIDDEN
        assert resp.json()["message"] == error_messages.CREDENTIAL_MISSING
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода авторизации пользователя")
class TestUserLogin:

    @allure.title("Авторизация существующего пользователя")
    def test_user_login_success(self, new_user):
        resp = User().user_login(new_user["email"], new_user["password"])
        assert resp.status_code == status_codes.CODE_OK
        assert resp.json()["user"]["email"] == new_user["email"]
        validate_schema(resp.json(), "user_login")

    @allure.title("Авторизация пользователя с некорректными данными")
    @pytest.mark.parametrize("invalid", [({"email": gen_creds()[0]}),
                                         ({"password": gen_creds()[1]}),
                                         ({"email": gen_creds()[0], "password": gen_creds()[1]})],
                             ids=["Неверный email", "Неверный password", "Неверные email и password"])
    def test_user_login_wrong_creds(self, new_user, invalid):
        credentials = {**new_user, **invalid}
        resp = User().user_login(credentials["email"], credentials["password"])
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.CREDENTIAL_INCORRECT
        validate_schema(resp.json(), "error_message")


@allure.suite("Проверки метода редактирования пользователя")
class TestUserUpdate:

    @allure.title("Редактирование авторизованного пользователя")
    @pytest.mark.parametrize("update_fields", [({"email": gen_creds()[0]}),
                                               ({"password": gen_creds()[1]}),
                                               ({"name": gen_creds()[2]}),],
                             ids=["Изменение email", "Изменение password", "Изменение name"])
    def test_user_update_success(self, new_user, update_fields):
        fields = {**new_user, **update_fields}
        resp = User().user_update(fields["email"], fields["password"], fields["name"], token=new_user["accessToken"])
        assert resp.status_code == status_codes.CODE_OK
        assert resp.json()["user"]["email"] == fields["email"] and resp.json()["user"]["name"] == fields["name"]
        validate_schema(resp.json(), "user_edit")

    @allure.title("Редактирование неавторизованного пользователя")
    def test_user_update_without_auth(self, new_user):
        resp = User().user_update(gen_creds()[0], gen_creds()[1], gen_creds()[2])
        assert resp.status_code == status_codes.CODE_UNAUTHORIZED
        assert resp.json()["message"] == error_messages.UNAUTHORIZED
        validate_schema(resp.json(), "error_message")
