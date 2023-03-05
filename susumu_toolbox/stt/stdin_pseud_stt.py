from susumu_toolbox.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.utility.config import Config


class StdinPseudSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)

    def recognize(self, audio_stream=None):
        self._event_channel.publish(self.EVENT_STT_START)

        input_text = input()
        self._event_channel.publish(self.EVENT_STT_RESULT, STTResult(input_text, True))

        self._event_channel.publish(self.EVENT_STT_END)
