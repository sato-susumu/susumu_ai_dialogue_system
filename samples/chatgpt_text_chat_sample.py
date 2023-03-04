import os

from samples.base_text_chat_sample import BaseTextChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ChatGPTTextChatSample(BaseTextChatSample):
    """ChatGPTテキストチャットのサンプル

    入力：標準入力
    応答生成：ChatGPT
    応答生成前後の翻訳：なし
    出力：画面出力
    """

    def __init__(self):
        super().__init__()

    def create_chat(self) -> BaseChat:
        system = SystemSettings()
        path = os.path.join(system.get_config_dir(), "sample_system_settings.txt")
        system.load_settings(path)
        return ChatGPTChat(self._config.get_openai_api_key(), system.get_system_settings())

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return StdinPseudSTT()

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator()


if __name__ == "__main__":
    ChatGPTTextChatSample().run_forever()
