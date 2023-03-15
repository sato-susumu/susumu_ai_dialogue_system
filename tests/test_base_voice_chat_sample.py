import threading
import time

from samples.base_voice_chat_sample import BaseVoiceChatSample
from susumu_toolbox.utility.config import Config
from tests.test_base_text_chat_sample import common_bye_1, common_bye_2, common_close


def start_sample():
    _config = Config()
    voice_chat_sample = BaseVoiceChatSample(_config)

    thread = threading.Thread(target=voice_chat_sample.run_once)
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
