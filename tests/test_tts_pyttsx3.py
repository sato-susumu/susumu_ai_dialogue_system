from susumu_ai_dialogue_system.infrastructure.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_tts_play():
    config = Config()
    Pyttsx3TTS(config)
