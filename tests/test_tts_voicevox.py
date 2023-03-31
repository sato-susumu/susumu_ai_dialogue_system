from susumu_toolbox.infrastructure.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.infrastructure.config import Config


def test_tts_play():
    config = Config()
    VoicevoxTTS(config)
