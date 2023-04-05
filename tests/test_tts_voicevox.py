from susumu_ai_dialogue_system.infrastructure.tts.voicevox_tts import VoicevoxTTS
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_tts_play():
    config = Config()
    VoicevoxTTS(config)
