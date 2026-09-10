import unittest
from unittest.mock import patch

from app import create_app
from app.extensions import db
from app.models import ensure_default_users, get_patient
from app.models import Patient, Reminder, get_patient


class ReminderFeatureTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            ensure_default_users()

    def test_caregiver_can_add_patient_reminder(self):
        self.client.post(
            "/login",
            data={"username": "caregiver", "password": "caregiver123"},
            follow_redirects=True,
        )

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

    @patch("app.services.text_to_speech.generate_reminder_audio", return_value=b"fake-audio")
    def test_patient_can_play_reminder_voice(self, mock_generate_audio):
        with self.app.app_context():
            patient = get_patient()
            reminder = Reminder(
                patient_id=patient.id,
                title="Take medicine",
                day="Tuesday",
                time="09:00",
                message="Please take the red tablet with water.",
            )
            db.session.add(reminder)
            db.session.commit()
            reminder_id = reminder.id

        response = self.client.get(f"/patient/reminder/{reminder_id}/voice")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "audio/wav")
        self.assertEqual(response.data, b"fake-audio")
        mock_generate_audio.assert_called_once()

    def test_patient_cannot_play_another_patient_reminder_voice(self):
        with self.app.app_context():
            get_patient()
            other_patient = Patient(name="Other patient")
            db.session.add(other_patient)
            db.session.commit()
            reminder = Reminder(
                patient_id=other_patient.id,
                title="Private reminder",
            )
            db.session.add(reminder)
            db.session.commit()
            reminder_id = reminder.id

        response = self.client.get(f"/patient/reminder/{reminder_id}/voice")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
