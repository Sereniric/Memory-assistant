import random


DIFFICULTIES = {
    "easy": 3,
    "medium": 5,
    "hard": 7
}

LEVELS = ["easy", "medium", "hard"]


def generate_sequence(difficulty):
    length = DIFFICULTIES[difficulty]
    return random.sample(range(10), length)


def calculate_score(sequence, answer):
    correct = 0

    for expected, actual in zip(sequence, answer):
        if expected == actual:
            correct += 1

    accuracy = (correct / len(sequence)) * 100

    return correct, accuracy


def next_difficulty(current, accuracy):
    current_index = LEVELS.index(current)

    if accuracy >= 80:
        current_index = min(current_index + 1, len(LEVELS) - 1)

    elif accuracy < 50:
        current_index = max(current_index - 1, 0)

    return LEVELS[current_index]