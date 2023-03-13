from susumu_toolbox.tts.gtts_tts import GttsTTS
from susumu_toolbox.utility.config import Config


def test_tts_play():
    config = Config()
    GttsTTS(config)
