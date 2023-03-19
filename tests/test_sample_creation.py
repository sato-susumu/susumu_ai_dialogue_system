from susumu_toolbox.sample.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.sample.stt.whisper_stt_sample import WhisperSTTSample
from susumu_toolbox.sample.voice_chat_sample import VoiceChatSample
from susumu_toolbox.utility.config import Config


def test_sample_creation_1():
    config = Config()
    VoiceChatSample(config)


def test_sample_creation_9():
    config = Config()
    BaseSTTSample(config)


def test_sample_creation_13():
    config = Config()
    WhisperSTTSample(config)
