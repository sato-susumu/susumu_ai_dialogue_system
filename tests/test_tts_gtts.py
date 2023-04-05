from susumu_ai_dialogue_system.infrastructure.tts.gtts_tts import GttsTTS
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_tts_play():
    config = Config()
    GttsTTS(config)
