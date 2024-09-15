import allure
import requests

from consts import Endpoints
from helper import create_user_data


class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_new_user(self, create_user):
        payload, response = create_user
        assert 200 == response.status_code and all([field in response.json() for field in "success user accessToken refreshToken".split()])

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_the_same_user_cannot_be_created(self, create_user):
        expected_response = {"success": False, "message": "User already exists"}
        payload, _ = create_user
        response = requests.post(Endpoints.CREATE_USER, payload)
        assert 403 == response.status_code and response.json() == expected_response

    @allure.title('Проверка обязательности полей')
    def test_presence_of_required_fields(self):
        expected_response = {"success": False, "message": "Email, password and name are required fields"}
        data = create_user_data()
        for field in ['email', 'password', 'name']:
            value = data.pop(field)
            response = requests.post(Endpoints.CREATE_USER, data)
            assert 403 == response.status_code and response.json() == expected_response
            data[field] = value
