import unittest

from app import create_app
from app.extensions import db
from app.models import EmergencyAlert, get_patient


class SosFeatureTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_home_shows_emergency_sos_button(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emergency SOS", response.data)

    def test_sos_requires_family_phone(self):
        response = self.client.get("/sos/confirm")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/patient/profile/edit?sos_setup=1", response.location)

    def test_sos_countdown_records_emergency_alert(self):
        with self.app.app_context():
            patient = get_patient()
            patient.caregiver_name = "Priya Sharma"
            patient.caregiver_phone = "+919876543210"
            db.session.commit()

        countdown = self.client.get("/sos/confirm")
        self.assertEqual(countdown.status_code, 200)
        self.assertIn(b"10 second countdown", countdown.data)
        self.assertIn(b"url=/sos/send", countdown.data)

        sent = self.client.get("/sos/send")
        self.assertEqual(sent.status_code, 200)
        self.assertIn(b"Emergency text message sent", sent.data)
        self.assertNotIn(b"Open text message", sent.data)

        with self.app.app_context():
            alert = EmergencyAlert.query.one()
            self.assertEqual(alert.recipient_name, "Priya Sharma")
            self.assertEqual(alert.recipient_phone, "+919876543210")
            self.assertIn("may need immediate help", alert.message)


if __name__ == "__main__":
    unittest.main()