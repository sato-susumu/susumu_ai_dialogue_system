import time
import traceback

from loguru import logger

from susumu_toolbox.application.base_chat_framework import BaseChatFramework
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import STTResult, STTEvent


# noinspection PyMethodMayBeStatic,DuplicatedCode
class VoiceChatFramework(BaseChatFramework):
    def __init__(self, config: Config):
        super().__init__(config)

        self._stt.event_subscribe(STTEvent.START, self._on_stt_start)
        self._stt.event_subscribe(STTEvent.END, self._on_stt_end)
        self._stt.event_subscribe(STTEvent.RESULT, self._on_stt_result)
        self._stt.event_subscribe(STTEvent.DEBUG_MESSAGE, self._on_stt_debug_message)
        self._stt.event_subscribe(STTEvent.ERROR, self._on_stt_error)

    def _on_stt_result(self, result: STTResult):
        super()._on_stt_result(result)
        self._obs.set_user_utterance_text(result.text)

    def run_once(self) -> None:
        super().run_once()
        # noinspection PyBroadException
        try:
            self._connect_all()

            while self._chat.is_connecting() and not self._termination_flag.is_set():
                time.sleep(1)

            while self._chat.is_connected() and not self._termination_flag.is_set():
                ai_result = self._wait_ai_response()
                if ai_result is None:
                    break

                ai_text = ai_result.text
                self._present_ai_message(ai_text, obs_ai_utterance_text=ai_text, tts_async_playback=False)

                user_text = self._wait_user_input()
                if user_text == "bye" or self._termination_flag.is_set():
                    self._termination_flag.set()
                    break

                self._request_ai_message(user_text=user_text, obs_ai_utterance_text="(考え中。。。)")
        except Exception:
            logger.error(traceback.format_exc())  # いつものTracebackが表示される
            logger.info("エラーが発生しましたが処理を継続します！")
        finally:
            self._disconnect_all()


if __name__ == "__main__":
    _config = Config()
    _config.search_and_load()
    _config.set_wrime_model_dir_path("../../model_data/wrime_model.pth")
    VoiceChatFramework(_config).run_forever()
