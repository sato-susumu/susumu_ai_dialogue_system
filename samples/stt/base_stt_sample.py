from susumu_toolbox.stt.base_stt import STTResult, BaseSTT


# noinspection PyMethodMayBeStatic,PyRedeclaration
class BaseSTTSample:
    def __init__(self):
        pass

    def on_start(self):
        print("stt start")

    def on_end(self):
        print("stt end")

    def on_result(self, result: STTResult):
        if result.is_timed_out:
            print('stt final(timeout):' + result.text)
        elif result.is_final:
            print('stt final:' + result.text)
        else:
            print('stt not final:' + result.text)

    def on_debug_message(self, x):
        # # デバッグ出力
        # print("------------------")
        # print(x)
        pass

    def on_error(self, e):
        print(e)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return BaseSTT()

    def run_forever(self) -> None:
        speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]

        stt = self.create_stt(speech_contexts=speech_contexts)
        stt.subscribe(stt.EVENT_STT_START, self.on_start)
        stt.subscribe(stt.EVENT_STT_END, self.on_end)
        stt.subscribe(stt.EVENT_STT_RESULT, self.on_result)
        stt.subscribe(stt.EVENT_STT_DEBUG_MESSAGE, self.on_debug_message)
        stt.subscribe(stt.EVENT_STT_ERROR, self.on_error)

        print("start recognition")
        while True:
            stt.recognize()
