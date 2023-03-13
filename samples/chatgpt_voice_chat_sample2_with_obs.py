from samples.chatgpt_voice_chat_sample2 import ChatGPTVoiceChatSample2
from susumu_toolbox.chat.base_chat import ChatResult
from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.stt.base_stt import STTResult
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ChatGPTVoiceChatSample2WithOBS(ChatGPTVoiceChatSample2):
    """ChatGPTボイスチャットのサンプル  字幕の仮実装付き

    入力：音声認識(GoogleStreamingSTT)
    応答生成：ChatGPT
    応答生成前後の翻訳：なし
    出力：画面出力、音声合成(VoicevoxTTS)、OBS
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._chat.subscribe(self._chat.EVENT_CHAT_MESSAGE, self._on_chat_message_for_obs)
        self._stt.subscribe(self._stt.EVENT_STT_START, self._on_stt_start_for_obs)
        self._stt.subscribe(self._stt.EVENT_STT_END, self._on_stt_end_for_obs)
        self._stt.subscribe(self._stt.EVENT_STT_RESULT, self._on_stt_result_for_obs)

        self._obs = OBSClient(self._config)
        self._stt_text = ""

    def _on_chat_message_for_obs(self, result: ChatResult):
        text = result.text
        # print(f"_on_chat_message_for_obs text={text}")
        self._obs.set_text("scene1", "text2", text)

    def _on_stt_start_for_obs(self):
        # print("_on_stt_start_for_obs")
        self._obs.set_text("scene1", "text1", "(マイクに向かって何か話してください)")

    def _on_stt_end_for_obs(self):
        # print("_on_stt_end_for_obs")
        if self._stt_text != "":
            self._obs.set_text("scene1", "text2", "(考え中。。。)")

    def _on_stt_result_for_obs(self, result: STTResult):
        text = result.text
        print(f"_on_stt_result_for_obs text={text}")
        self._obs.set_text("scene1", "text1", text)
        self._stt_text = text

    def run_forever(self) -> None:
        self._obs.connect()
        self._obs.set_text("scene1", "text1", "")
        self._obs.set_text("scene1", "text2", "")
        try:
            super().run_forever()
        finally:
            self._obs.set_text("scene1", "text1", "")
            self._obs.set_text("scene1", "text2", "")
            self._obs.disconnect()


if __name__ == "__main__":
    _config = Config()
    _config.load()
    ChatGPTVoiceChatSample2WithOBS(_config).run_forever()
