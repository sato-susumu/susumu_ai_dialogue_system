from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.sr_google_sync_stt import SRGoogleSyncSTT


# noinspection PyMethodMayBeStatic
class GoogleTentativeSTTSample(BaseSTTSample):
    """speech_recognition音声認識(google)のサンプル"""

    def __init__(self):
        super().__init__()

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return SRGoogleSyncSTT()


if __name__ == "__main__":
    GoogleTentativeSTTSample().run_forever()
