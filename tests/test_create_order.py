import allure
import requests

from consts import Endpoints
from helper import generate_random_string


class TestCreateOrder:

    @allure.title('Создание заказа авторизованным пользователем')
    def test_authorizated_user_create_order(self, authorization, get_id_of_ingredients):
        response = requests.post(Endpoints.CREATE_ORDER, headers=authorization, data=get_id_of_ingredients)
        assert 200 == response.status_code and response.json()['success'] and 'number' in response.json()['order']

    @allure.title('Создание заказа неавторизованным пользователем')
    def test_unauthorizated_user_get_order(self, get_id_of_ingredients):
        response = requests.post(Endpoints.CREATE_ORDER, data=get_id_of_ingredients)
        assert 200 == response.status_code and response.json()['success'] and 'number' in response.json()['order']
    # Согласно требованиям, нет ограничений на создание заказа неавторизованным пользователем.
    # В Постамане заказ успешно создается, при этом на сайте (с фронта) заказ сделать нельзя.
    # Оставила статус-код 200, чтобы тест "не падал" (тред: https://app.pachca.com/chats/10628756?message=325304209)

    @allure.title('Создание заказа с добавлением ингредиентов')
    def test_create_order_with_ingredients(self):
        pass
        # Потому что тест будет проверять то же самое, что и test_authorizated_user_create_order, так как без ингредиентов
        # заказ создать нельзя (либо копируем код).
        # Пы.сы. Я бы вообще этот тест не добавляла к проверкам, но, вероятно, он нужен для документирования

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, authorization):
        expected_result = {"success": False, "message": "Ingredient ids must be provided"}
        response = requests.post(Endpoints.CREATE_ORDER, headers=authorization)
        assert 400 == response.status_code and response.json() == expected_result

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_incorrect_hash_of_ingredients(self, authorization):
        response = requests.post(Endpoints.CREATE_ORDER, headers=authorization, data={'ingredients':[generate_random_string(10)]})
        assert 500 == response.status_code
