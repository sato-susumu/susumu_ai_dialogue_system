from susumu_toolbox.infrastructure.translation.googletrans_translator import GoogletransTranslator
from susumu_toolbox.infrastructure.config import Config


def test_translator():
    config = Config()
    GoogletransTranslator(config)
