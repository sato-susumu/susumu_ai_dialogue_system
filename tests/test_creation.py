from susumu_ai_dialogue_system.application.ai_tuber_framework import AiVTuberFramework
from susumu_ai_dialogue_system.application.common.log_mannager import LogManager
from susumu_ai_dialogue_system.application.text_chat_framework import TextChatFramework
from susumu_ai_dialogue_system.application.voice_chat_framework import VoiceChatFramework
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.vad.webrtc_vad import WebRtcVad


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
