from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.youtube_pseud_stt import YoutubePseudSTT

from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class YoutubePseudSTTSample(BaseSTTSample):

    # noinspection PyShadowingNames
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return YoutubePseudSTT(self._config)


if __name__ == "__main__":
    config = Config()
    config.load()
    YoutubePseudSTTSample(config).run_forever()
