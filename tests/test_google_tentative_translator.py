from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator


# noinspection SpellCheckingInspection
def test_translate_ja_en():
    translator = GoogletransTranslator()
    text = translator.translate("コマ", target_lang=translator.LANG_CODE_EN_US)
    assert text == "Koma"


def test_translate_en_ja():
    translator = GoogletransTranslator()
    text = translator.translate("coma", target_lang=translator.LANG_CODE_JA_JP)
    assert text == "とともに"
