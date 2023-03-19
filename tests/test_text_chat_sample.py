import threading
import time

from samples.text_chat_sample import TextChatSample
from susumu_toolbox.chat.base_chat import ChatResult
from susumu_toolbox.stt.base_stt import STTResult
from susumu_toolbox.utility.config import Config


def start_sample():
    _config = Config()
    _config.set_common_input_function(_config.INPUT_FUNCTION_BASE)
    _config.set_common_output_function(_config.OUTPUT_FUNCTION_BASE)
    _config.set_common_obs_enabled(False)
    text_chat_sample = TextChatSample(_config)

    thread = threading.Thread(target=text_chat_sample.run_once)
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
