from susumu_toolbox.application.voice_chat_sample import VoiceChatSample
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.system_setting import SystemSettings


def test_sample_creation_1():
    config = Config()
    system_settings = SystemSettings(config)
    VoiceChatSample(config, system_settings)
