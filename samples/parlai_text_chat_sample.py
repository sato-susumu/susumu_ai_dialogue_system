from samples.base_text_chat_sample import BaseTextChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.parlai_chat import ParlAIChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ParlAITextChatSample(BaseTextChatSample):
    """テキストチャットのサンプル

    入力：標準入力
    応答生成：ParlAI
    応答生成前後の翻訳：DeepL
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
        return StdinPseudSTT()

    def create_translator(self) -> BaseTranslator:
        return GoogletransTranslator()


if __name__ == "__main__":
    ParlAITextChatSample().run_forever()
