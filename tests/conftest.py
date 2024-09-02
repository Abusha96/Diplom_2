import pytest
import requests

from consts import Endpoints
from helper import create_user_data


@pytest.fixture(scope="function")
def create_user():
    new_user = create_user_data()
    response = requests.post(Endpoints.CREATE_USER, new_user)
    yield new_user, response
    requests.post(Endpoints.LOGIN_USER, data=new_user)
    requests.delete(Endpoints.USER_DATA)


@pytest.fixture(scope="function")
def authorization():
    new_user = create_user_data()
    requests.post(Endpoints.CREATE_USER, new_user)
    response = requests.post(Endpoints.LOGIN_USER, data=new_user)
    yield {'Authorization': response.json()['accessToken']}
    requests.delete(Endpoints.USER_DATA)


@pytest.fixture(scope="function")
def get_id_of_ingredients():
    response = requests.get(Endpoints.GET_INGREDIENTS)
    result = [i['_id'] for i in response.json()['data']]
    result = {'ingredients': result}
    yield result
