from susumu_toolbox.application.ai_tuber_framework import AiVTuberFramework
from susumu_toolbox.application.common.log_mannager import LogManager
from susumu_toolbox.application.text_chat_framework import TextChatFramework
from susumu_toolbox.application.voice_chat_framework import VoiceChatFramework
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.vad.webrtc_vad import WebRtcVad


def test_voice_chat_sample():
    config = Config()
    VoiceChatFramework(config)


def test_ai_v_tuber_sample():
    config = Config()
    AiVTuberFramework(config)


def test_text_chat_sample():
    config = Config()
    TextChatFramework(config)


def test_log_manager():
    LogManager().setup_logger()


def test_web_rtc_vad():
    WebRtcVad()
