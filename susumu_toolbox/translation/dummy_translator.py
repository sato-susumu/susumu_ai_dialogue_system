from typing import Optional

from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.utility.config import Config


class DummyTranslator(BaseTranslator):
    def __init__(self, config: Config):
        super().__init__(config)

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        return text
