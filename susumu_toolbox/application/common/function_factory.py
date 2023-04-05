from susumu_toolbox.application.common.log_controller import LogController
from susumu_toolbox.infrastructure.app_controller.dummy_app_contorller import DummyAppController
from susumu_toolbox.infrastructure.app_controller.threaded_app_controller import ThreadedAppController
from susumu_toolbox.infrastructure.app_controller.vmagicmirror_controller import VMagicMirrorController
from susumu_toolbox.infrastructure.chat.base_chat import BaseChat
from susumu_toolbox.infrastructure.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.infrastructure.chat.parlai_chat import ParlAIChat
from susumu_toolbox.infrastructure.config import Config, OutputFunction, InputFunction, ChatFunction
from susumu_toolbox.infrastructure.emotion.dummy_emotion_model import DummyEmotionModel
from susumu_toolbox.infrastructure.emotion.wrime_emotion_model import WrimeEmotionModel
from susumu_toolbox.infrastructure.obs.base_obs_client import BaseOBSClient
from susumu_toolbox.infrastructure.obs.dummy_obs_client import DummyOBSClient
from susumu_toolbox.infrastructure.obs.obs_client import OBSClient
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT
from susumu_toolbox.infrastructure.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.infrastructure.stt.sr_google_sync_stt import SRGoogleSyncSTT
from susumu_toolbox.infrastructure.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.infrastructure.stt.whisper_stt import WhisperApiSTT
from susumu_toolbox.infrastructure.stt.youtube_pseud_stt import YoutubePseudSTT
from susumu_toolbox.infrastructure.tts.base_tts import BaseTTS
from susumu_toolbox.infrastructure.tts.dummy_tts import DummyTTS
from susumu_toolbox.infrastructure.tts.google_cloud_tts import GoogleCloudTTS
from susumu_toolbox.infrastructure.tts.gtts_tts import GttsTTS
from susumu_toolbox.infrastructure.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_toolbox.infrastructure.tts.voicevox_tts import VoicevoxTTS


class FunctionFactory:

    @staticmethod
    def create_stt(config: Config, speech_contexts) -> BaseSTT:
        input_function = config.get_common_input_function()
        if input_function == InputFunction.BASE:
            return BaseSTT(config)
        if input_function == InputFunction.SR_GOOGLE:
            return SRGoogleSyncSTT(config)
        if input_function == InputFunction.STDIN_PSEUD:
            return StdinPseudSTT(config)
        if input_function == InputFunction.GOOGLE_STREAMING:
            return GoogleStreamingSTT(config, speech_contexts=speech_contexts)
        if input_function == InputFunction.YOUTUBE_PSEUD:
            return YoutubePseudSTT(config)
        if input_function == InputFunction.WHISPER_API:
            return WhisperApiSTT(config)
        raise ValueError(f"Invalid input_function: {input_function}")

    @staticmethod
    def create_chat(config: Config) -> BaseChat:
        chat_function = config.get_common_chat_function()
        if chat_function == ChatFunction.PARLAI:
            return ParlAIChat(config)
        if chat_function == ChatFunction.CHATGPT:
            return ChatGPTChat(config)
        raise ValueError(f"Invalid chat_function: {chat_function}")

    @staticmethod
    def create_tts(config: Config) -> BaseTTS:
        output_function = config.get_common_output_function()
        if output_function == OutputFunction.BASE:
            return BaseTTS(config)
        if output_function == OutputFunction.GOOGLE_CLOUD:
            return GoogleCloudTTS(config)
        if output_function == OutputFunction.GTTS:
            return GttsTTS(config)
        if output_function == OutputFunction.PYTTSX3:
            return Pyttsx3TTS(config)
        if output_function == OutputFunction.VOICEVOX:
            return VoicevoxTTS(config)
        if output_function == OutputFunction.NONE:
            return DummyTTS(config)
        raise ValueError(f"Invalid output_function: {output_function}")

    @staticmethod
    def create_obs_client(config: Config) -> BaseOBSClient:
        obs_enabled = config.get_common_obs_enabled()
        if obs_enabled:
            return OBSClient(config)
        return DummyOBSClient(config)

    @staticmethod
    def create_emotion_model(config: Config):
        value = config.get_common_v_magic_mirror_connection_enabled()
        if value:
            return WrimeEmotionModel(config)
        return DummyEmotionModel(config)

    @staticmethod
    def create_app_controller(config: Config):
        value = config.get_common_v_magic_mirror_connection_enabled()
        if value:
            source_controller = VMagicMirrorController(config)
            return ThreadedAppController(config, source_controller)
        return DummyAppController(config)

    @staticmethod
    def create_log_controller(config: Config):
        return LogController(config)
