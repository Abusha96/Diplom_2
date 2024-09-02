import allure
import pytest
import requests

from consts import Endpoints
from helper import generate_random_string


class TestEditUser:

    @allure.title('Изменение данных авторизованным пользователем')
    @pytest.mark.parametrize('field, value', [
    ['email', f'{generate_random_string}mail.ru'],
    ['name', generate_random_string(10)],
    ['password', generate_random_string(10)]
    ])
    def test_edit_authorizated_user(self, authorization, field, value):
        response = requests.patch(Endpoints.USER_DATA, headers=authorization, data={field:value})
        assert 200 == response.status_code and all([field in response.json() for field in "success user".split()])

    @allure.title('Изменение данных неавторизованным пользователем')
    def test_edit_unauthorizated_user(self):
        expected_response = {"success": False, "message": "You should be authorised"}
        response = requests.patch(Endpoints.USER_DATA)
        assert 401 == response.status_code and response.json() == expected_response

    @allure.title('Изменение почты на ту, которая уже существует')
    def test_email_already_exists(self, authorization, create_user):
        expected_response = {"success": False, "message": "User with such email already exists"}
        payload, _ = create_user
        response = requests.patch(Endpoints.USER_DATA, headers=authorization, data={'email':payload['email']})
        assert 403 == response.status_code and response.json() == expected_response
