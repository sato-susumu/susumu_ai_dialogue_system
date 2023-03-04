from typing import Optional

from susumu_toolbox.translation.base_translator import BaseTranslator


class DummyTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        return text
