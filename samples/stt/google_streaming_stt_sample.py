from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT

# noinspection PyMethodMayBeStatic
from susumu_toolbox.utility.config import Config


class GoogleStreamingSTTSample(BaseSTTSample):
    """Googleストリーミング音声認識のサンプル"""

    # noinspection PyShadowingNames
    def __init__(self, config: Config):
        super().__init__(config)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return GoogleStreamingSTT(self._config, speech_contexts=speech_contexts)


if __name__ == "__main__":
    config = Config()
    config.load_config()
    GoogleStreamingSTTSample(config).run_forever()
