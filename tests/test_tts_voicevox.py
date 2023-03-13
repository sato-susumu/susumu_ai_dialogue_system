from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.utility.config import Config


def test_tts_play():
    config = Config()
    VoicevoxTTS(config)
