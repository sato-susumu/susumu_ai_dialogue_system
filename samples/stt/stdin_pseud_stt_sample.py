from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT


# noinspection PyMethodMayBeStatic
class StdinPseudSTTSample(BaseSTTSample):
    """標準入力を使った疑似音声認識のサンプル"""

    def __init__(self):
        super().__init__()

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return StdinPseudSTT()


if __name__ == "__main__":
    StdinPseudSTTSample().run_forever()
