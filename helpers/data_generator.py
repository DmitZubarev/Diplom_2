import random
import string


def generate_credentials():
    name = "user_" + "".join(random.choices(string.ascii_lowercase, k=6))
    domain = random.choice(['yandex.ru','mail.ru', 'gmail.com'])
    email = f'{name}@{domain}'
    password = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))
    return email, password, name

def generate_ingredients(amount=3):
    ingredients = []
    for i in range(amount):
        ingredients.append(generate_string(24))
    return ingredients

def generate_string(length=12):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
