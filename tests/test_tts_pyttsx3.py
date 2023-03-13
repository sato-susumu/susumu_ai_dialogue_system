from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_toolbox.utility.config import Config


def test_tts_play():
    config = Config()
    Pyttsx3TTS(config)
