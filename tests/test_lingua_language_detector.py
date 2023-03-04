from susumu_toolbox.language_detector.lingua_language_detector import LinguaLanguageDetector


def test_translate_ja_en():
    detector = LinguaLanguageDetector()
    result = detector.detect("コマ")
    assert result == detector.LANG_CODE_JP


def test_translate_en_ja():
    detector = LinguaLanguageDetector()
    result = detector.detect("coma")
    assert result == detector.LANG_CODE_EN
