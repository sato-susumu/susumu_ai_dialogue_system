# noinspection PyPackageRequirements
from lingua import Language, LanguageDetectorBuilder

from susumu_toolbox.infrastructure.language_detector.base_language_detector import BaseLanguageDetector


class LinguaLanguageDetector(BaseLanguageDetector):
    def __init__(self):
        super().__init__()
        language_list = [Language.ENGLISH, Language.JAPANESE]
        self._detector = LanguageDetectorBuilder.from_languages(*language_list).build()

    def detect(self, text: str) -> str:
        result = self._detector.detect_language_of(text)
        if result == Language.JAPANESE:
            return self.LANG_CODE_JA
        return self.LANG_CODE_EN
