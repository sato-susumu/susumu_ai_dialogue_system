from susumu_ai_dialogue_system.infrastructure.translation.googletrans_translator import GoogletransTranslator
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_translator():
    config = Config()
    GoogletransTranslator(config)
