from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast


class SpeechToTextError(Exception):
    """Raised when uploaded speech cannot be converted or recognized."""


def transcribe_audio(audio_file, language="en-IN"):
    try:
        import speech_recognition as speech
        from pydub import AudioSegment
    except ImportError as error:
        raise SpeechToTextError(
            "Speech recognition dependencies are not installed."
        ) from error

    suffix = Path(audio_file.filename or "answer.audio").suffix or ".audio"

    with TemporaryDirectory() as directory:
        source_path = Path(directory) / f"source{suffix}"
        wav_path = Path(directory) / "answer.wav"
        audio_file.save(source_path)

        try:
            AudioSegment.from_file(source_path).export(wav_path, format="wav")
        except Exception as error:
            raise SpeechToTextError(
                "The uploaded audio format could not be converted."
            ) from error

        recognizer = cast(Any, speech.Recognizer())

        try:
            with speech.AudioFile(str(wav_path)) as source:
                audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language=language)
        except (speech.UnknownValueError, speech.RequestError) as error:
            raise SpeechToTextError(
                "The speech service could not recognize the answer."
            ) from error
