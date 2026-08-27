import random


PICTURES = [
    "🌞",
    "🌙",
    "🌼",
    "🌳",
    "🍎",
    "🍉",
    "🐶",
    "🐱",
    "☀️",
    "🌧️",
    "⭐",
    "🎈",
    "🌸",
    "🍇",
    "🍊",
    "🌟",
    "🦋",
    "🌍",
    "🧁",
    "🍪",
]


def create_round(level):
    number_of_items = min(3 + level, 6)

    remember_items = random.sample(
        PICTURES,
        number_of_items
    )

    wrong_items = random.sample(
        [
            item for item in PICTURES
            if item not in remember_items
        ],
        4
    )

    options = remember_items + wrong_items
    random.shuffle(options)

    return {
        "remember_items": remember_items,
        "options": options,
    }


def calculate_points(level):
    return 100 * level


def check_answer(selected, remember_items):
    return set(selected) == set(remember_items)
