from helpers.data_generator import generate_string


def order_create(ingredients: list[str]=None, amount=3, generate=True):
    if generate:
        new_ingredients = []
        for i in range(amount):
            new_ingredients.append(generate_string(24))

        if ingredients is None or not ingredients:
            ingredients = new_ingredients

    return {
        "ingredients": ingredients
    }
