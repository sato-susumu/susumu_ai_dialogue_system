import threading
import time

from samples.base_text_chat_sample import BaseTextChatSample
from susumu_toolbox.chat.base_chat import ChatResult
from susumu_toolbox.stt.base_stt import STTResult
from tests.test_utility import get_test_config


def start_sample():
    _config = get_test_config()
    text_chat_sample = BaseTextChatSample(_config)

    thread = threading.Thread(target=text_chat_sample.run_forever)
    thread.start()

    # 接続待ち
    # noinspection PyProtectedMember
    while not text_chat_sample._chat.is_connected():
        time.sleep(0.1)

    return text_chat_sample, thread


# 最初の発話でbye
# noinspection PyProtectedMember
def common_bye_1(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("bye", True))

    thread.join()


# 2回目の発話でbye
# noinspection PyProtectedMember
def common_bye_2(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("test", True))

    # チャットからの返事
    sample._chat_message_queue.put(ChatResult("test2", []))

    # 発話
    sample._stt_message_queue.put(STTResult("bye", True, is_timed_out=True))

    thread.join()


# 発話後にチャットからクローズ
# noinspection PyProtectedMember
def common_close(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("test", False))

    # チャットからの返事ではなく、切断
    sample._chat_message_queue.put(None)

    thread.join()


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
