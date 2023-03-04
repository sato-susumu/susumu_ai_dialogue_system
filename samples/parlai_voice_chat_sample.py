from samples.base_voice_chat_sample import BaseVoiceChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.parlai_chat import ParlAIChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.sr_google_sync_stt import SRGoogleSyncSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ParlAIVoiceChatSample(BaseVoiceChatSample):
    """ボイスチャットのサンプル

    入力：音声認識(SRGoogleSyncSTT)
    応答生成：ParlAI
    応答生成前後の翻訳：GoogleTentativeTranslator
    出力：画面出力、音声合成(Pyttsx3TTS)
    """

    def __init__(self):
        super().__init__()

    def create_chat(self) -> BaseChat:
        return ParlAIChat(
            self._config.get_parlai_host(),
            self._config.get_parlai_port_no()
        )

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return SRGoogleSyncSTT()

    def create_tts(self) -> BaseTTS:
        return Pyttsx3TTS()

    def create_translator(self) -> BaseTranslator:
        return GoogletransTranslator()


if __name__ == "__main__":
    ParlAIVoiceChatSample().run_forever()
