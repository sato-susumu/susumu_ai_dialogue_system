from susumu_toolbox.language_detector.base_language_detector import BaseLanguageDetector
from susumu_toolbox.language_detector.lingua_language_detector import LinguaLanguageDetector


def test_base_language_detector_jp():
    detector = BaseLanguageDetector()
    detector.detect("コマ")


def test_base_language_detector_en():
    detector = BaseLanguageDetector()
    detector.detect("coma")


def test_lingua_language_detector_jp():
    detector = LinguaLanguageDetector()
    result = detector.detect("コマ")
    assert result == detector.LANG_CODE_JA


def test_lingua_language_detector_en():
    detector = LinguaLanguageDetector()
    result = detector.detect("coma")
    assert result == detector.LANG_CODE_EN
