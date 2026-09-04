import unittest

from flask import Flask

from app.games.result_tracking import get_results, record_result
from app.routes.sequence_recall import normalize_answer


class ResultTrackingTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "test-secret"

    def test_record_result_saves_result_in_session(self):
        with self.app.test_request_context():
            record_result(
                "Sequence Recall",
                score=2,
                accuracy=66.666,
                difficulty="easy",
            )

            results = get_results()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["game"], "Sequence Recall")
        self.assertEqual(results[0]["score"], 2)
        self.assertEqual(results[0]["accuracy"], 66.67)
        self.assertEqual(results[0]["difficulty"], "easy")
        self.assertIn("completed_at", results[0])

    def test_results_start_empty(self):
        with self.app.test_request_context():
            self.assertEqual(get_results(), [])

    def test_normalize_answer_accepts_digits(self):
        self.assertEqual(normalize_answer("4 8 2 7"), [4, 8, 2, 7])

    def test_normalize_answer_accepts_spoken_digits(self):
        self.assertEqual(
            normalize_answer("four eight two seven"),
            [4, 8, 2, 7],
        )

    def test_normalize_answer_rejects_non_numbers(self):
        with self.assertRaises(ValueError):
            normalize_answer("four apples")


if __name__ == "__main__":
    unittest.main()
