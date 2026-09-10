import unittest

from app import create_app
from app.localization import get_active_language, translate_text


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_defaults_to_assamese_language(self):
        with self.client.session_transaction() as session:
            self.assertNotIn("lang", session)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session.get("lang"), "as")

    def test_translation_falls_back_to_assamese_text(self):
        self.assertEqual(get_active_language({}), "as")
        self.assertEqual(translate_text("nav.home", "as"), "ঘৰ")
        self.assertEqual(translate_text("nav.home", "en"), "Home")


if __name__ == "__main__":
    unittest.main()
