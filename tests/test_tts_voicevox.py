from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from tests.test_utility import get_test_config


def test_tts_play():
    config = get_test_config()
    VoicevoxTTS(config)
