from loguru import logger

from susumu_toolbox.application.common.function_factory import FunctionFactory
from susumu_toolbox.application.common.stt_helper import STTHelper
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import STTResult, STTEvent


# noinspection PyMethodMayBeStatic
class STTTest:
    def __init__(self, config: Config):
        self._config = config

        self._stt = None
        self._stt_helper = None

    def run(self) -> None:
        speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]
        self._stt = FunctionFactory.create_stt(self._config, speech_contexts)
        self._stt_helper = STTHelper(self._config)

        # noinspection DuplicatedCode
        self._stt.event_subscribe(STTEvent.START, self._on_stt_start)
        self._stt.event_subscribe(STTEvent.END, self._on_stt_end)
        self._stt.event_subscribe(STTEvent.RESULT, self._on_stt_result)
        self._stt.event_subscribe(STTEvent.DEBUG_MESSAGE, self._on_stt_debug_message)
        self._stt.event_subscribe(STTEvent.ERROR, self._on_stt_error)
        self._stt.recognize()

    def _on_stt_start(self):
        logger.debug("入力準備完了")
        start_message = self._stt_helper.get_start_message_for_console()
        logger.debug(f"{start_message}")

    def _on_stt_end(self):
        pass

    def _on_stt_result(self, result: STTResult):
        if result.is_timed_out:
            logger.debug("タイムアウトしました")
        elif not result.is_final:
            logger.debug(f"中間結果: {result.text}")
        else:
            logger.debug(f"結果: {result.text}")

    def _on_stt_debug_message(self, x):
        pass

    def _on_stt_error(self, e):
        pass


if __name__ == "__main__":
    _config = Config()
    _config.search_and_load()
    STTTest(_config).run()
