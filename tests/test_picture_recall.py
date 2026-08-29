import unittest

from app.games.picture_recall import (
    calculate_points,
    check_answer,
    create_round,
)


class PictureRecallGameTest(unittest.TestCase):
    def test_create_round_returns_unique_items(self):
        round_data = create_round(1)

        self.assertGreaterEqual(len(round_data["remember_items"]), 3)
        self.assertEqual(
            len(round_data["remember_items"]),
            len(set(round_data["remember_items"])),
        )
        self.assertGreaterEqual(len(round_data["options"]), 6)

    def test_check_answer_accepts_correct_items(self):
        selected = ["🌞", "🌙", "🌼"]
        remember_items = ["🌞", "🌙", "🌼"]

        self.assertTrue(check_answer(selected, remember_items))

    def test_calculate_points_scales_with_level(self):
        self.assertEqual(calculate_points(2), 200)


if __name__ == "__main__":
    unittest.main()
