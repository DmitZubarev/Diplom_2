import random
import string


def generate_credentials():
    name = "user_" + "".join(random.choices(string.ascii_lowercase, k=6))
    email = f'{name}@yandex.ru'
    password = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))
    return email, password, name
