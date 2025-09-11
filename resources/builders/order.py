from resources.steps.ingredients import Ingredients


def order_create(ingredients: list[str]=None, amount=3, autofill=True):
    if autofill:
        new_ingredients = Ingredients().ingredients_get_list(amount)

        if ingredients is None or not ingredients:
            ingredients = new_ingredients

    return {
        "ingredients": ingredients
    }
