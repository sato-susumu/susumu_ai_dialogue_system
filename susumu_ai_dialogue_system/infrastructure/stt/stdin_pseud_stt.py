from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.stt.base_stt import BaseSTT, STTResult, STTEvent


class StdinPseudSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)

    @BaseSTT.recognize_decorator
    def recognize(self):
        self._event_publish(STTEvent.START)
        input_text = input()
        self._event_publish(STTEvent.RESULT, STTResult(input_text, True))
