from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import STTResult, BaseSTT


# noinspection PyMethodMayBeStatic,PyRedeclaration
class BaseSTTSample:
    def __init__(self, config: Config):
        self._config = config

    def _on_start(self):
        print("stt start")

    def _on_end(self):
        print("stt end")

    def _on_result(self, result: STTResult):
        if result.is_timed_out:
            print('stt final(timeout):' + result.text)
        elif result.is_final:
            print('stt final:' + result.text)
        else:
            print('stt not final:' + result.text)

    def _on_debug_message(self, x):
        # # デバッグ出力
        # print("------------------")
        # print(x)
        pass

    def _on_error(self, e):
        print(e)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return BaseSTT(self._config)

    def run_forever(self) -> None:
        speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]

        # speech_contextsが用意できるタイミングでSTTを生成する
        stt = self.create_stt(speech_contexts=speech_contexts)
        stt.subscribe(stt.EVENT_STT_START, self._on_start)
        stt.subscribe(stt.EVENT_STT_END, self._on_end)
        stt.subscribe(stt.EVENT_STT_RESULT, self._on_result)
        stt.subscribe(stt.EVENT_STT_DEBUG_MESSAGE, self._on_debug_message)
        stt.subscribe(stt.EVENT_STT_ERROR, self._on_error)

        print("start recognition")
        while True:
            stt.recognize()
