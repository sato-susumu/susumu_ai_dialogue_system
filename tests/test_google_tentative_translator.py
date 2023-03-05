from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator
from susumu_toolbox.utility.config import Config


# noinspection SpellCheckingInspection
def test_translate_ja_en():
    config = Config()
    config.load_config()

    translator = GoogletransTranslator(config)
    text = translator.translate("コマ", target_lang=translator.LANG_CODE_EN_US)
    assert text == "Koma"


def test_translate_en_ja():
    config = Config()
    config.load_config()

    translator = GoogletransTranslator(config)
    text = translator.translate("coma", target_lang=translator.LANG_CODE_JA_JP)
    assert text == "とともに"
