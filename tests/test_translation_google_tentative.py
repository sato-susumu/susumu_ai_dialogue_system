from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator
from susumu_toolbox.utility.config import Config


def test_translator():
    config = Config()
    GoogletransTranslator(config)
