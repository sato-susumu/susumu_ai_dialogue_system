from susumu_toolbox.infrastructure.tts.gtts_tts import GttsTTS
from susumu_toolbox.infrastructure.config import Config


def test_tts_play():
    config = Config()
    GttsTTS(config)
