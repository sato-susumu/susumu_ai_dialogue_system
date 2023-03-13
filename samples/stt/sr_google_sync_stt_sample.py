from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.sr_google_sync_stt import SRGoogleSyncSTT

from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class SRGoogleSyncSTTSample(BaseSTTSample):
    """speech_recognition音声認識(google)のサンプル"""

    # noinspection PyShadowingNames
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return SRGoogleSyncSTT(self._config)


if __name__ == "__main__":
    config = Config()
    config.load()
    SRGoogleSyncSTTSample(config).run_forever()
