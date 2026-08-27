import random


ITEMS = [
    "Apple",
    "Milk",
    "Bread",
    "Carrot",
    "Banana",
    "Eggs",
    "Rice",
    "Cheese",
    "Tomato",
    "Potato",
    "Juice",
    "Biscuits",
    "Butter",
    "Chocolate",
    "Cereal",
    "Soap",
    "Coffee",
    "Sugar"
]


def create_round(level):
    number_of_items = min(3 + level, 10)

    remember_items = random.sample(
        ITEMS,
        number_of_items
    )

    wrong_items = random.sample(
        [
            item for item in ITEMS
            if item not in remember_items
        ],
        4
    )

    options = remember_items + wrong_items

    random.shuffle(options)

    return {
        "remember_items": remember_items,
        "options": options
    }


def calculate_points(level):
    return 100 * level


def check_answer(selected, remember_items):
    return set(selected) == set(remember_items)