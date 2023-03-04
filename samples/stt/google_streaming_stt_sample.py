from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT


# noinspection PyMethodMayBeStatic
class GoogleStreamingSTTSample(BaseSTTSample):
    """Googleストリーミング音声認識のサンプル"""

    def __init__(self):
        super().__init__()

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return GoogleStreamingSTT(speech_contexts=speech_contexts)


if __name__ == "__main__":
    GoogleStreamingSTTSample().run_forever()
