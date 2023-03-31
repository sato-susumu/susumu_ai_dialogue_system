from typing import Optional

import deepl

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.translation.base_translator import BaseTranslator


class DeepLTranslator(BaseTranslator):
    def __init__(self, config: Config):
        super().__init__(config)
        self._translator = deepl.Translator(self._config.get_deepl_auth_key())

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        # TODO: base_langに対応
        if text == "":
            return ""
        target_lang = target_lang.replace(self.LANG_CODE_JA_JP, "JA")
        target_lang = target_lang.replace(self.LANG_CODE_EN_US, "EN-US")
        result = self._translator.translate_text(text, target_lang=target_lang)
        return result.text
