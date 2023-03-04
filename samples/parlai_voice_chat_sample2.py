from samples.parlai_voice_chat_sample import ParlAIVoiceChatSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.deepl_translator import DeepLTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ParlAIVoiceChatSample2(ParlAIVoiceChatSample):
    """ボイスチャットのサンプル2

    入力：音声認識(GoogleStreamingSTT)
    応答生成：ParlAI
    応答生成前後の翻訳：DeepL
    出力：画面出力、音声合成(VoicevoxTTS)
    """

    def __init__(self):
        super().__init__()

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return GoogleStreamingSTT()

    def create_tts(self) -> BaseTTS:
        return VoicevoxTTS()

    def create_translator(self) -> BaseTranslator:
        return DeepLTranslator(self._config.get_deepl_auth_key())


if __name__ == "__main__":
    ParlAIVoiceChatSample2().run_forever()
