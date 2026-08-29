import unittest

from flask import Flask

from app.games.result_tracking import get_results, record_result


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


if __name__ == "__main__":
    unittest.main()
