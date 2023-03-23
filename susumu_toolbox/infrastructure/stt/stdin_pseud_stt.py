from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT, STTResult


class StdinPseudSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)

    @BaseSTT.recognize_decorator
    def recognize(self):
        self._event_channel.publish(self.EVENT_STT_START)
        input_text = input()
        self._event_channel.publish(self.EVENT_STT_RESULT, STTResult(input_text, True))
