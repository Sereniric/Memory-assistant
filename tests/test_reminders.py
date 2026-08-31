import unittest

from app import create_app
from app.extensions import db
from app.models import get_patient


class ReminderFeatureTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_caregiver_can_add_patient_reminder(self):
        response = self.client.post(
            "/caregiver/reminder/add",
            data={
                "title": "Morning medicine",
                "day": "Monday",
                "time": "08:30",
                "message": "Give the daily tablet after breakfast.",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            patient = get_patient()
            self.assertEqual(len(patient.reminders), 1)
            self.assertEqual(patient.reminders[0].title, "Morning medicine")
            self.assertEqual(patient.reminders[0].time, "08:30")
            self.assertEqual(patient.reminders[0].day, "Monday")


if __name__ == "__main__":
    unittest.main()
