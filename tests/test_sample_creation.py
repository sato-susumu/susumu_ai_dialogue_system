from samples.base_voice_chat_sample import BaseVoiceChatSample
from samples.chatgpt_text_chat_sample import ChatGPTTextChatSample
from samples.chatgpt_voice_chat_sample import ChatGPTVoiceChatSample
from samples.chatgpt_voice_chat_sample2 import ChatGPTVoiceChatSample2
from samples.chatgpt_voice_chat_sample2_with_obs import ChatGPTVoiceChatSample2WithOBS
from samples.parlai_text_chat_sample import ParlAITextChatSample
from samples.parlai_voice_chat_sample import ParlAIVoiceChatSample
from samples.parlai_voice_chat_sample2 import ParlAIVoiceChatSample2
from samples.stt.base_stt_sample import BaseSTTSample
from samples.stt.google_streaming_stt_sample import GoogleStreamingSTTSample
from samples.stt.google_tentative_stt_sample import GoogleTentativeSTTSample
from samples.stt.stdin_pseud_stt_sample import StdinPseudSTTSample

from tests.test_utility import get_test_config


def test_sample_creation_1():
    config = get_test_config()
    BaseVoiceChatSample(config)


def test_sample_creation_2():
    config = get_test_config()
    ChatGPTTextChatSample(config)


def test_sample_creation_3():
    config = get_test_config()
    ChatGPTVoiceChatSample(config)


def test_sample_creation_4():
    config = get_test_config()
    ChatGPTVoiceChatSample2(config)


def test_sample_creation_5():
    config = get_test_config()
    ChatGPTVoiceChatSample2WithOBS(config)


def test_sample_creation_6():
    config = get_test_config()
    ParlAITextChatSample(config)


def test_sample_creation_7():
    config = get_test_config()
    ParlAIVoiceChatSample(config)


def test_sample_creation_8():
    config = get_test_config()
    ParlAIVoiceChatSample2(config)


def test_sample_creation_9():
    config = get_test_config()
    BaseSTTSample(config)


def test_sample_creation_10():
    config = get_test_config()
    GoogleStreamingSTTSample(config)


def test_sample_creation_11():
    config = get_test_config()
    GoogleTentativeSTTSample(config)


def test_sample_creation_12():
    config = get_test_config()
    StdinPseudSTTSample(config)
