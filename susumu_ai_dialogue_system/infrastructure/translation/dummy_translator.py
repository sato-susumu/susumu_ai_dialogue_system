from typing import Optional

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.translation.base_translator import BaseTranslator


class DummyTranslator(BaseTranslator):
    def __init__(self, config: Config):
        super().__init__(config)

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        return text
