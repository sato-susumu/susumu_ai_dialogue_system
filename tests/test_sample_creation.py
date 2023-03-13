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
from samples.stt.sr_google_sync_stt_sample import SRGoogleSyncSTTSample
from samples.stt.stdin_pseud_stt_sample import StdinPseudSTTSample
from samples.stt.whisper_stt_sample import WhisperSTTSample
from samples.stt.youtube_pseud_stt_sample import YoutubePseudSTTSample
from susumu_toolbox.utility.config import Config


def test_sample_creation_1():
    config = Config()
    BaseVoiceChatSample(config)


def test_sample_creation_2():
    config = Config()
    ChatGPTTextChatSample(config)


def test_sample_creation_3():
    config = Config()
    ChatGPTVoiceChatSample(config)


def test_sample_creation_4():
    config = Config()
    ChatGPTVoiceChatSample2(config)


def test_sample_creation_5():
    config = Config()
    ChatGPTVoiceChatSample2WithOBS(config)


def test_sample_creation_6():
    config = Config()
    ParlAITextChatSample(config)


def test_sample_creation_7():
    config = Config()
    ParlAIVoiceChatSample(config)


def test_sample_creation_8():
    config = Config()
    ParlAIVoiceChatSample2(config)


def test_sample_creation_9():
    config = Config()
    BaseSTTSample(config)


def test_sample_creation_10():
    config = Config()
    GoogleStreamingSTTSample(config)


def test_sample_creation_11():
    config = Config()
    SRGoogleSyncSTTSample(config)


def test_sample_creation_12():
    config = Config()
    StdinPseudSTTSample(config)


def test_sample_creation_13():
    config = Config()
    WhisperSTTSample(config)


def test_sample_creation_14():
    config = Config()
    YoutubePseudSTTSample(config)
