from samples.base_voice_chat_sample import BaseVoiceChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.parlai_chat import ParlAIChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.deepl_translator import DeepLTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ParlAIVoiceChatSample2(BaseVoiceChatSample):
    """ボイスチャットのサンプル2

    入力：音声認識(GoogleStreamingSTT)
    応答生成：ParlAI
    応答生成前後の翻訳：DeepL
    出力：画面出力、音声合成(VoicevoxTTS)
    """

    def __init__(self):
        super().__init__()

    def create_chat(self) -> BaseChat:
        return ParlAIChat(self._config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return GoogleStreamingSTT(self._config)

    def create_tts(self) -> BaseTTS:
        return VoicevoxTTS(self._config)

    def create_translator(self) -> BaseTranslator:
        return DeepLTranslator(self._config)


if __name__ == "__main__":
    ParlAIVoiceChatSample2().run_forever()
