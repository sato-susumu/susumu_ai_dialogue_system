from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.chat.parlai_chat import ParlAIChat
from susumu_toolbox.obs.base_obs_client import BaseOBSClient
from susumu_toolbox.obs.dummy_obs_client import DummyOBSClient
from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.google_streaming_stt import GoogleStreamingSTT
from susumu_toolbox.stt.sr_google_sync_stt import SRGoogleSyncSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT
from susumu_toolbox.stt.youtube_pseud_stt import YoutubePseudSTT
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS
from susumu_toolbox.tts.gtts_tts import GttsTTS
from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.system_setting import SystemSettings


class FunctionFactory:

    @staticmethod
    def create_stt(config: Config, speech_contexts) -> BaseSTT:
        input_function = config.get_common_input_function()
        if input_function == Config.INPUT_FUNCTION_BASE:
            return BaseSTT(config)
        if input_function == Config.INPUT_FUNCTION_SR_GOOGLE:
            return SRGoogleSyncSTT(config)
        if input_function == Config.INPUT_FUNCTION_STDIN_PSEUD:
            return StdinPseudSTT(config)
        if input_function == Config.INPUT_FUNCTION_GOOGLE_STREAMING:
            return GoogleStreamingSTT(config, speech_contexts=speech_contexts)
        if input_function == Config.INPUT_FUNCTION_YOUTUBE_PSEUD:
            return YoutubePseudSTT(config)
        raise ValueError(f"Invalid input_function: {input_function}")

    @staticmethod
    def create_chat(config: Config, system: SystemSettings) -> BaseChat:
        chat_function = config.get_common_chat_function()
        if chat_function == Config.CHAT_FUNCTION_PARLAI:
            return ParlAIChat(config)
        if chat_function == Config.CHAT_FUNCTION_CHATGPT:
            return ChatGPTChat(config, system)
        raise ValueError(f"Invalid chat_function: {chat_function}")

    @staticmethod
    def create_tts(config: Config) -> BaseTTS:
        output_function = config.get_common_output_function()
        if output_function == Config.OUTPUT_FUNCTION_BASE:
            return BaseTTS(config)
        if output_function == Config.OUTPUT_FUNCTION_GOOGLE_CLOUD:
            return GoogleCloudTTS(config)
        if output_function == Config.OUTPUT_FUNCTION_GTTS:
            return GttsTTS(config)
        if output_function == Config.OUTPUT_FUNCTION_PYTTSX3:
            return Pyttsx3TTS(config)
        if output_function == Config.OUTPUT_FUNCTION_VOICEVOX:
            return VoicevoxTTS(config)
        raise ValueError(f"Invalid output_function: {output_function}")

    @staticmethod
    def create_obs_client(config: Config) -> BaseOBSClient:
        obs_enabled = config.get_common_obs_enabled()
        if obs_enabled:
            return OBSClient(config)
        return DummyOBSClient(config)
