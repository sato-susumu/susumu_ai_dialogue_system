from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS
from tests.test_utility import get_test_config


def test_tts_play():
    config = get_test_config()
    Pyttsx3TTS(config)
