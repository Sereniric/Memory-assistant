from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory


class TextToSpeechError(Exception):
    """Raised when reminder text cannot be converted to speech."""


def generate_reminder_audio(reminder):
    try:
        import pyttsx3
    except ImportError as error:
        raise TextToSpeechError(
            "Text-to-speech dependencies are not installed."
        ) from error

    spoken_parts = [reminder.title]
    schedule = " ".join(
        value for value in (reminder.day, reminder.time) if value
    )
    if schedule:
        spoken_parts.append(schedule)
    if reminder.message:
        spoken_parts.append(reminder.message)

    with TemporaryDirectory() as directory:
        audio_path = Path(directory) / "reminder.wav"
        try:
            engine = pyttsx3.init()
            engine.save_to_file(". ".join(spoken_parts), str(audio_path))
            engine.runAndWait()
            audio_data = audio_path.read_bytes()
        except Exception as error:
            raise TextToSpeechError(
                "The reminder could not be converted to speech."
            ) from error

    return BytesIO(audio_data)