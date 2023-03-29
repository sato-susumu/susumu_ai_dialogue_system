import logging

from susumu_toolbox.application.common.function_factory import FunctionFactory
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.tts.base_tts import TTSEvent


# noinspection PyMethodMayBeStatic
class TTSTest:
    def __init__(self, config: Config):
        self._config = config
        self._logger = logging.getLogger(__name__)

        self._tts = FunctionFactory.create_tts(self._config)
        self._tts.event_subscribe(TTSEvent.START, self._on_tts_start)
        self._tts.event_subscribe(TTSEvent.END, self._on_tts_end)

    def run(self) -> None:
        self._tts.tts_play_async("テストです。")

    def _on_tts_start(self):
        self._logger.debug("再生開始")

    def _on_tts_end(self):
        self._logger.debug("再生完了")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    _config = Config()
    _config.search_and_load()
    TTSTest(_config).run()
