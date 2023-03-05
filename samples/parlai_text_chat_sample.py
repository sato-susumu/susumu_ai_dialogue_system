from samples.base_text_chat_sample import BaseTextChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.parlai_chat import ParlAIChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.googletrans_translator import GoogletransTranslator
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ParlAITextChatSample(BaseTextChatSample):
    """テキストチャットのサンプル

    入力：標準入力
    応答生成：ParlAI
    応答生成前後の翻訳：DeepL
    出力：画面出力、音声合成(Pyttsx3TTS)
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def create_chat(self) -> BaseChat:
        return ParlAIChat(self._config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return StdinPseudSTT(self._config)

    def create_translator(self) -> BaseTranslator:
        return GoogletransTranslator(self._config)


if __name__ == "__main__":
    _config = Config()
    _config.load_config()
    ParlAITextChatSample(_config).run_forever()
