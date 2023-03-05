import threading
import time

from samples.base_voice_chat_sample import BaseVoiceChatSample
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.utility.config import Config
from tests.test_base_text_chat_sample import common_bye_1, common_bye_2, common_close


class VoiceChatSample(BaseVoiceChatSample):
    def __init__(self, config: Config):
        super().__init__(config)

    def create_chat(self) -> BaseChat:
        return BaseChat(self._config)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return BaseSTT(self._config)

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)


def start_sample():
    _config = Config()
    _config.load_config()
    voice_chat_sample = VoiceChatSample(_config)

    thread = threading.Thread(target=voice_chat_sample.run_forever)
    thread.start()

    # 接続待ち
    # noinspection PyProtectedMember
    while not voice_chat_sample._chat.is_connected():
        time.sleep(0.1)

    return voice_chat_sample, thread


# noinspection DuplicatedCode
def test_bye_1():
    sample, thread = start_sample()
    common_bye_1(sample, thread)


def test_bye_2():
    sample, thread = start_sample()
    common_bye_2(sample, thread)


def test_close():
    sample, thread = start_sample()
    common_close(sample, thread)
