from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator
from tests.test_utility import get_test_config


def test_translator():
    config = get_test_config()
    GoogletransTranslator(config)
