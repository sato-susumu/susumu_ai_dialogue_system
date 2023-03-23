from susumu_toolbox.application.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT
from susumu_toolbox.infrastructure.stt.whisper_stt import WhisperSTT


# noinspection PyMethodMayBeStatic
class WhisperSTTSample(BaseSTTSample):
    """Whisper API音声認識のサンプル"""

    # noinspection PyShadowingNames
    def __init__(self, config: Config):
        super().__init__(config)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return WhisperSTT(self._config)


if __name__ == "__main__":
    config = Config()
    config.search_and_load()
    WhisperSTTSample(config).run_forever()
