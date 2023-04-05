import threading
import time

from susumu_ai_dialogue_system.application.voice_chat_framework import VoiceChatFramework
from susumu_ai_dialogue_system.infrastructure.config import Config, OutputFunction, InputFunction
from tests.test_text_chat_sample import common_bye_1, common_bye_2, common_close


def start_sample():
    _config = Config()
    _config.set_common_input_function(InputFunction.BASE)
    _config.set_common_output_function(OutputFunction.BASE)
    _config.set_common_obs_enabled(False)
    voice_chat_sample = VoiceChatFramework(_config)

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
