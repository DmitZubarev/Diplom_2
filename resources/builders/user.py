from helpers.data_generator import generate_credentials


def user_create(email=None, password=None, name=None, autofill=True):
    if autofill:
        new_email, new_password, new_name = generate_credentials()

        if email is None:
            email = new_email
        if password is None:
            password = new_password
        if name is None:
            name = new_name

    return {
        "email": email,
        "password": password,
        "name": name
    }

def user_login(email=None, password=None, autofill=True):
    if autofill:
        new_email, new_password, _ = generate_credentials()

        if email is None:
            email = new_email
        if password is None:
            password = new_password

    return {
        "email": email,
        "password": password
    }
