import unittest
from io import BytesIO
from unittest.mock import patch

from app import create_app


class VoiceInputTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.client.session_transaction() as session:
            session["sequence"] = [4, 8, 2]
            session["difficulty"] = "easy"

    @patch("app.routes.sequence_recall.transcribe_audio")
    def test_voice_upload_renders_normalized_confirmation(
        self,
        transcribe_audio,
    ):
        transcribe_audio.return_value = "four eight two"

        with self.client.session_transaction() as session:
            session["lang"] = "en"

        response = self.client.post(
            "/game/voice",
            data={
                "voice_answer": (
                    BytesIO(b"audio"),
                    "answer.webm",
                ),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You said:", response.data)
        self.assertIn(b"four eight two", response.data)
        self.assertIn(b'value="4 8 2"', response.data)
        transcribe_audio.assert_called_once_with(
            unittest.mock.ANY,
            language="en-IN",
        )

    def test_voice_upload_without_file_returns_to_answer_page(self):
        response = self.client.post("/game/voice", data={})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please record or choose an audio answer.", response.data)


if __name__ == "__main__":
    unittest.main()
