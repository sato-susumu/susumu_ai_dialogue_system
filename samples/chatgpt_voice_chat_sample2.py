import os

from samples.base_voice_chat_sample import BaseVoiceChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ChatGPTVoiceChatSample2(BaseVoiceChatSample):
    """ChatGPTボイスチャットのサンプル

    入力：音声認識(GoogleStreamingSTT)
    応答生成：ChatGPT
    応答生成前後の翻訳：なし
    出力：画面出力、音声合成(VoicevoxTTS)
    """

    def __init__(self):
        super().__init__()

    def create_chat(self) -> BaseChat:
        system = SystemSettings()
        path = os.path.join(system.get_config_dir(), "sample_system_settings.txt")
        system.load_settings(path)
        return ChatGPTChat(self._config.get_openai_api_key(), system.get_system_settings())

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return GoogleStreamingSTT(self._config)

    def create_tts(self) -> BaseTTS:
        return VoicevoxTTS(self._config)

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)


if __name__ == "__main__":
    ChatGPTVoiceChatSample2().run_forever()
