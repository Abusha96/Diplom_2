import allure
import requests

from consts import Endpoints
from helper import generate_random_string


class TestLoginUser:
    @allure.title('Логин под существующим пользователем')
    def test_success_authorization(self, create_user):
        payload, _ = create_user
        response = requests.post(Endpoints.LOGIN_USER, payload)
        assert 200 == response.status_code and all([field in response.json() for field in "success user accessToken refreshToken".split()])

    @allure.title('Логин с неверным логином и паролем')
    def test_incorrect_creds(self, create_user):
        expected_response = {"success": False, "message": "email or password are incorrect"}
        payload, _ = create_user
        for field in ['email', 'password']:
            value = payload.pop(field)
            payload[field] = generate_random_string(10)
            if field == 'email':
                payload[field] += '@mail.ru'
            response = requests.post(Endpoints.LOGIN_USER, payload)
            assert 401 == response.status_code and response.json() == expected_response
            payload[field] = value
