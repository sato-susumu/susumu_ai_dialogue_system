from typing import Optional

from googletrans import Translator

from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.utility.config import Config


class GoogletransTranslator(BaseTranslator):
    def __init__(self, config: Config):
        super().__init__(config)
        self._translator = Translator()

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        if text == "":
            return ""
        target_lang = target_lang.replace(self.LANG_CODE_JA_JP, "ja")
        target_lang = target_lang.replace(self.LANG_CODE_EN_US, "en")
        if base_lang is None:
            result = self._translator.translate(text, dest=target_lang)
            return result.text

        base_lang = base_lang.replace(self.LANG_CODE_JA_JP, "ja")
        base_lang = base_lang.replace(self.LANG_CODE_EN_US, "en")
        result = self._translator.translate(text, dest=target_lang, src=base_lang)
        return result.text
