import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def create_user_data():
    # генерируем логин, пароль и имя юзера
    email = f'{generate_random_string(10)}@mail.ru'
    password = generate_random_string(10)
    name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload
