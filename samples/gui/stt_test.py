from samples.gui.gui_events import GuiEvents
from susumu_toolbox.stt.base_stt import STTResult
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.stt.sr_google_sync_stt import SRGoogleSyncSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.stt.youtube_pseud_stt import YoutubePseudSTT
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class STTTest:
    def __init__(self, config: Config):
        self._config = config
        self._stt = None
        self._start_message = ""

    def run(self, event) -> None:
        if event == GuiEvents.YOUTUBE_PSEUD_STT_TEST:
            self._stt = YoutubePseudSTT(self._config)
            self._start_message = "YouTubeライブチャットのコメント入力待ち"
        elif event == GuiEvents.GOOGLE_STREAMING_STT_TEST:
            speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]
            self._stt = GoogleStreamingSTT(self._config, speech_contexts=speech_contexts)
            self._start_message = "マイクに向かって何か話しかけてください"
        elif event == GuiEvents.SR_GOOGLE_STT_TEST:
            self._stt = SRGoogleSyncSTT(self._config)
            self._start_message = "マイクに向かって何か話しかけてください"
        else:
            self._stt = StdinPseudSTT(self._config)
            self._start_message = "このウィンドウで何か入力して、リターンキーを押してください"

        # noinspection DuplicatedCode
        self._stt.subscribe(self._stt.EVENT_STT_START, self._on_stt_start)
        self._stt.subscribe(self._stt.EVENT_STT_END, self._on_stt_end)
        self._stt.subscribe(self._stt.EVENT_STT_RESULT, self._on_stt_result)
        self._stt.subscribe(self._stt.EVENT_STT_DEBUG_MESSAGE, self._on_stt_debug_message)
        self._stt.subscribe(self._stt.EVENT_STT_ERROR, self._on_stt_error)
        self._stt.recognize()

    def _on_stt_start(self):
        print("入力準備完了")
        print(f"{self._start_message}")

    def _on_stt_end(self):
        pass

    def _on_stt_result(self, result: STTResult):
        if result.is_timed_out:
            print("タイムアウトしました")
        elif not result.is_final:
            print(f"中間結果: {result.text}")
        else:
            print(f"結果: {result.text}")

    def _on_stt_debug_message(self, x):
        pass

    def _on_stt_error(self, e):
        pass
