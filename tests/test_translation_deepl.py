from susumu_toolbox.infrastructure.translation.deepl_translator import DeepLTranslator
from susumu_toolbox.infrastructure.config import Config


def test_deepl():
    config = Config()
    config.set_deepl_auth_key("test")
    DeepLTranslator(config)
