import time

from app.games.sequence_recall import (
    generate_sequence,
    calculate_score,
    next_difficulty
)


def play_round(difficulty):
    sequence = generate_sequence(difficulty)

    print("\n" + "=" * 40)
    print(f"Difficulty: {difficulty.upper()}")
    print("=" * 40)

    print("\nRemember this sequence:")
    print(" ".join(map(str, sequence)))

    input("\nPress ENTER when you are ready to answer...")

    print("\n" * 30)

    answer_text = input(
        "Enter the numbers in the same order, separated by spaces: "
    )

    try:
        answer = [int(number) for number in answer_text.split()]
    except ValueError:
        print("\nPlease enter numbers only.")
        return difficulty

    correct, accuracy = calculate_score(sequence, answer)

    print("\n" + "=" * 40)
    print("RESULT")
    print("=" * 40)

    print(f"Correct: {correct}/{len(sequence)}")
    print(f"Accuracy: {accuracy:.0f}%")

    if accuracy >= 80:
        print("🎉 Great job!")

    elif accuracy >= 50:
        print("👍 Good try!")

    else:
        print("💪 Keep practicing!")

    new_difficulty = next_difficulty(
        difficulty,
        accuracy
    )

    if new_difficulty != difficulty:
        print(
            f"\nDifficulty changes: "
            f"{difficulty.upper()} → {new_difficulty.upper()}"
        )
    else:
        print(
            f"\nDifficulty remains: "
            f"{difficulty.upper()}"
        )

    return new_difficulty


def main():
    difficulty = "easy"

    print("\n🧠 SEQUENCE RECALL GAME")
    print("========================")

    while True:
        difficulty = play_round(difficulty)

        choice = input(
            "\nPlay another round? (y/n): "
        ).strip().lower()

        if choice != "y":
            break

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()