from susumu_ai_dialogue_system.infrastructure.translation.deepl_translator import DeepLTranslator
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_deepl():
    config = Config()
    config.set_deepl_auth_key("test")
    DeepLTranslator(config)
