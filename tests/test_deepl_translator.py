from susumu_toolbox.translation.deepl_translator import DeepLTranslator
from susumu_toolbox.utility.config_manager import ConfigManager


def test_translate_ja_en():
    config = ConfigManager()
    config.load_config()

    translator = DeepLTranslator(config.get_deepl_auth_key())
    text = translator.translate("コマ", target_lang=translator.LANG_CODE_EN_US)
    assert text == "coma"


def test_translate_en_ja():
    config = ConfigManager()
    config.load_config()

    translator = DeepLTranslator(config.get_deepl_auth_key())
    text = translator.translate("coma", target_lang=translator.LANG_CODE_JA_JP)
    assert text == "コマ" or text == "コーマ"
