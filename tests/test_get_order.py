import allure
import requests

from consts import Endpoints


class TestGetOrder:

    @allure.title('Получение списка заказов авторизованным пользователем')
    def test_authorizated_user_get_order(self, authorization, get_id_of_ingredients):
        requests.post(Endpoints.CREATE_ORDER, headers=authorization, data=get_id_of_ingredients)
        response = requests.get(Endpoints.GET_ORDER, headers=authorization)
        assert 200 == response.status_code and response.json()['success'] and 'orders' in response.json()

    @allure.title('Получение списка заказов неавторизованным пользователем')
    def test_unauthorizated_user_get_order(self, authorization, get_id_of_ingredients):
        expected_result = {"success": False, "message": "You should be authorised"}
        requests.post(Endpoints.CREATE_ORDER, headers=authorization, data=get_id_of_ingredients)
        response = requests.get(Endpoints.GET_ORDER)
        assert 401 == response.status_code and expected_result == response.json()
