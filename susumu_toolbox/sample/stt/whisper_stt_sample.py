from susumu_toolbox.sample.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.whisper_stt import WhisperSTT
from susumu_toolbox.utility.config import Config


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
