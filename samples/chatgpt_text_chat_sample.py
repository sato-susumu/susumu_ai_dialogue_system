import os

from samples.parlai_text_chat_sample import ParlAITextChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic,DuplicatedCode
class ChatGPTTextChatSample(ParlAITextChatSample):
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

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator()


if __name__ == "__main__":
    ChatGPTTextChatSample().run_forever()
