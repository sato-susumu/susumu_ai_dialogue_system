from susumu_toolbox.translation.deepl_translator import DeepLTranslator
from tests.test_utility import get_test_config


def test_deepl():
    config = get_test_config()
    DeepLTranslator(config)
