from loguru import logger

from susumu_ai_dialogue_system.application.common.function_factory import FunctionFactory
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.base_tts import TTSEvent


# noinspection PyMethodMayBeStatic
class TTSTest:
    def __init__(self, config: Config):
        self._config = config

        self._tts = FunctionFactory.create_tts(self._config)
        self._tts.event_subscribe(TTSEvent.START, self._on_tts_start)
        self._tts.event_subscribe(TTSEvent.END, self._on_tts_end)

    def run(self, text) -> None:
        self._tts.tts_play_async(text)

    def _on_tts_start(self):
        logger.debug("再生開始")

    def _on_tts_end(self):
        logger.debug("再生完了")


if __name__ == "__main__":
    _config = Config()
    _config.search_and_load()
    TTSTest(_config).run("テストします")
