from __future__ import annotations

import copy
import os
from enum import Enum
from typing import List, Any
from typing import TYPE_CHECKING

from omegaconf import OmegaConf

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.infrastructure.system_setting import SystemSettings


class OutputFunction(Enum):
    BASE = "base_tts"
    NONE = "none"
    PYTTSX3 = "pyttsx3"
    VOICEVOX = "voicevox"
    GOOGLE_CLOUD = "google_cloud"
    GTTS = "gtts"

    @classmethod
    def str2function(cls, function_str: str) -> Any:
        for function in OutputFunction:
            if function.value == function_str:
                return function
        raise ValueError(f"{function_str} is not found in OutputFunction.")


class InputFunction(Enum):
    BASE = "base_stt"
    SR_GOOGLE = "sr_google"
    STDIN_PSEUD = "stdin_pseud"
    GOOGLE_STREAMING = "google_streaming"
    YOUTUBE_PSEUD = "youtube_pseud"
    WHISPER_API = "whisper_api"

    @classmethod
    def str2function(cls, function_str: str) -> Any:
        for function in InputFunction:
            if function.value == function_str:
                return function
        raise ValueError(f"{function_str} is not found in InputFunction.")


class BaseFunction(Enum):
    VOICE_DIALOGUE = "voice_dialogue"
    TEXT_DIALOGUE = "text_dialogue"
    AI_TUBER = "ai_tuber"

    @classmethod
    def str2function(cls, function_str: str) -> Any:
        for function in BaseFunction:
            if function.value == function_str:
                return function
        raise ValueError(f"{function_str} is not found in BaseFunction.")


class LangChainMemoryType(Enum):
    ConversationBufferWindowMemory = "conversation_buffer_window_memory"
    ConversationBufferMemory = "conversation_buffer_memory"
    ConversationSummaryMemory = "conversation_summary_memory"
    ConversationSummaryBufferMemory = "conversation_summary_buffer_memory"
    CombinedMemory = "combined_memory"

    @classmethod
    def name2memory_type(cls, memory_type_str: str) -> Any:
        for function in LangChainMemoryType:
            if function.name == memory_type_str:
                return function
        raise ValueError(f"{memory_type_str} is not found in LangChainMemory.")

    @classmethod
    def keys(cls):
        return [memory_type.name for memory_type in LangChainMemoryType]


# noinspection PyMethodMayBeStatic
class Config:
    _CONFIG_FILE_NAME = "config.yaml"
    KEY_OPENAI_API_KEY = "openai_api_key"
    KEY_DEEPL_AUTH_KEY = "deepl_auth_key"
    KEY_AI_SYSTEM_SETTINGS_TEXT = "ai_system_settings_text"
    KEY_VOICEVOX_HOST = "voicevox_host"
    KEY_VOICEVOX_PORT_NO = "voicevox_port_no"
    KEY_VOICEVOX_SPEAKER_NO = "voicevox_speaker_no"
    KEY_OBS_HOST = "obs_host"
    KEY_OBS_PORT_NO = "obs_port_no"
    KEY_OBS_PASSWORD = "obs_password"
    KEY_OBS_USER_UTTERANCE_SOURCE_NAME = "obs_user_utterance_source_name"
    KEY_OBS_AI_UTTERANCE_SOURCE_NAME = "obs_ai_utterance_source_name"
    KEY_YOUTUBE_LIVE_URL = "youtube_live_url"
    KEY_GCP_YOUTUBE_DATA_API_KEY = "gcp_youtube_data_api_key"
    KEY_COMMON_BASE_FUNCTION = "common_base_function"
    KEY_COMMON_CHAT_FUNCTION = "common_chat_function"
    KEY_COMMON_INPUT_FUNCTION = "common_input_function"
    KEY_COMMON_OUTPUT_FUNCTION = "common_output_function"
    KEY_COMMON_OBS_ENABLED = "common_obs_enabled"
    KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED = "common_v_magic_mirror_connection_enabled"
    KEY_WRIME_EMOTION_SERVER_HOST = "wrime_emotion_server_host"
    KEY_WRIME_EMOTION_SERVER_PORT_NO = "wrime_emotion_server_port_no"
    KEY_GCP_TEXT_TO_SPEECH_API_KEY = "gcp_text_to_speech_api_key"
    KEY_GCP_TEXT_TO_SPEECH_SPEAKER_NAME = "gcp_text_to_speech_speaker_name"
    KEY_GCP_SPEECH_TO_TEXT_API_KEY = "gcp_speech_to_text_api_key"
    KEY_GUI_APP_TITLE = "gui_app_title"
    KEY_GUI_THEME_NAME = "gui_theme_name"
    KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED = "pyaudio_secondary_output_enabled"
    KEY_PYAUDIO_SECONDARY_OUTPUT_API_NAME = "pyaudio_secondary_output_api_name"
    KEY_PYAUDIO_SECONDARY_OUTPUT_DEVICE_NAME = "pyaudio_secondary_output_device_name"
    KEY_ADVANCED_CONSOLE_LOG_LEVEL = "advanced_console_log_level"
    KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED = "advanced_chat_gpt_history_log_enabled"
    KEY_ADVANCED_LANGCHAIN_ENABLED = "advanced_langchain_enabled"
    KEY_LANGCHAIN_CONVERSATION_VERBOSE = "langchain_conversation_verbose"
    KEY_LANGCHAIN_MEMORY_TYPE = "langchain_memory_type"

    USER_DATA_DIR_NAME = "user_data"
    SAMPLE_DIR_NAME = "application"

    base_function_dict = {
        BaseFunction.VOICE_DIALOGUE.value: "音声対話",
        BaseFunction.AI_TUBER.value: "AI VTuber",
        BaseFunction.TEXT_DIALOGUE.value: "文字対話",
    }
    input_function_dict = {
        InputFunction.SR_GOOGLE.value: "サンプル音声認識 SpeechRecognition",
        InputFunction.STDIN_PSEUD.value: "文字入力",
        InputFunction.GOOGLE_STREAMING.value: "Google Speech-to-Text ストリーミング音声認識 (追加設定が必要)",
        InputFunction.WHISPER_API.value: "Whisper API音声認識 (OpenAI API Key設定が必要)",
        InputFunction.YOUTUBE_PSEUD.value: "YouTube ライブチャット入力取り込み (追加設定が必要)",
    }
    output_function_dict = {
        OutputFunction.NONE.value: "なし",
        OutputFunction.PYTTSX3.value: "サンプル音声合成 pyttsx3",
        OutputFunction.VOICEVOX.value: "VOICEVOX 音声合成 (VOICEVOXアプリ起動が必要)",
        OutputFunction.GOOGLE_CLOUD.value: "Google Text-to-Speech 音声合成 (追加設定が必要)",
        OutputFunction.GTTS.value: "サンプル音声合成 gTTS",
    }

    def __init__(self):
        # 仕方なくここでimport

        from susumu_ai_dialogue_system.infrastructure.ai_config_list import AiConfigList
        # 辞書からコンフィグを読み込む
        default_yaml = """
            Common:
              format_version: 1
              common_base_function: "voice_dialogue"
              common_input_function: "sr_google"
              common_chat_function: "chatgpt"
              common_output_function: "pyttsx3"
              common_obs_enabled: false
              common_v_magic_mirror_connection_enabled: false
            DeepL:
              deepl_auth_key: ""
            OpenAI:
              openai_api_key: ""
            OBS:
              obs_host: "127.0.0.1"
              obs_port_no: 4455
              obs_password: "パスワード"
              obs_user_utterance_source_name: "user_input_text"
              obs_ai_utterance_source_name: "ai_output_text"
            VOICEVOX:
              voicevox_host: "127.0.0.1"
              voicevox_port_no: 50021
              voicevox_speaker_no: 8
            YouTube:
              # GCP YouTube Data API v3のAPIキー
              gcp_youtube_data_api_key: ""
              # YouTubeのライブ配信URL。例：https://www.youtube.com/watch?v=xxxxxxxxxxx
              youtube_live_url: ""
            GoogleTextToSpeech:
              gcp_text_to_speech_api_key:
              gcp_text_to_speech_speaker_name: "ja-JP-Neural2-B"
            GoogleSpeechToText:
              gcp_speech_to_text_api_key:
            PyAudio:
              # 標準スピーカー以外にも同時出力するかどうか
              pyaudio_secondary_output_enabled: false
              # 名前の一部でもいい
              pyaudio_secondary_output_api_name: "MME"
              pyaudio_secondary_output_device_name: "VB-Audio Virtual C"
            WrimeEmotionServer:
              wrime_emotion_server_host: "127.0.0.1"
              wrime_emotion_server_port_no: 56563
            LangChain:
              langchain_conversation_verbose: false
              langchain_memory_type: "ConversationBufferWindowMemory"
            Advanced:
              advanced_chat_gpt_history_log_enabled: false
              advanced_console_log_level: "DEBUG"
              advanced_langchain_enabled: false
            GUI:
              gui_app_title: "susumu_ai_dialogue_system"
              gui_theme_name: "Bright Colors"   
        """
        self._config = OmegaConf.create(default_yaml)
        # 設定ファイルのパス。初回保存前だとファイルが存在しないこともあるので注意
        self._current_config_path = None
        self._ai_config_list = AiConfigList(self)
        self._wrime_model_dir_path = "./model_data/wrime_model.pth"

    def save(self) -> None:
        assert self._current_config_path is not None
        config_dir = os.path.dirname(self._current_config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        OmegaConf.save(self._config, self._current_config_path)
        self._ai_config_list.save()

    # noinspection DuplicatedCode
    def search_and_load(self) -> None:
        """設定ファイルを検索して読み込む

        GUI以外から起動したとき、GUIで保存した設定ファイルを読み込むために使用する
        """
        file_path = os.path.join(self.search_config_dir(), self._CONFIG_FILE_NAME)
        self.load(file_path)

    def load(self, file_path: str) -> None:
        loaded_config = OmegaConf.load(file_path)
        self._config = OmegaConf.merge(self._config, loaded_config)
        if self._ai_config_list.exist_ai_config_file():
            self._ai_config_list.load()

    def set_current_config_path(self, file_path: str) -> None:
        self._current_config_path = file_path

    def get_current_config_path(self) -> str:
        return self._current_config_path

    def get_default_config_path(self) -> str:
        return os.path.join(self.get_user_data_dir_path(), self._CONFIG_FILE_NAME)

    def get_user_data_dir_path(self) -> str:
        return f"./{self.USER_DATA_DIR_NAME}/"

    def get_ai_config_file_path(self, ai_id: str) -> str:
        return f"./{self.USER_DATA_DIR_NAME}/ai_config_{ai_id}.yaml"

    def get_ai_system_settings_file_path(self, ai_id: str) -> str:
        return f"./{self.USER_DATA_DIR_NAME}/ai_system_settings_{ai_id}.txt"

    def make_user_data_dir_if_not_exists(self) -> None:
        dir_path = self.get_user_data_dir_path()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_ai_id_list(self) -> List[str]:
        return self._ai_config_list.get_ai_id_list()

    def get_ai_system_settings(self, ai_id: str) -> SystemSettings:
        ai_config = self._ai_config_list.get_ai_config(ai_id)
        return ai_config.get_system_settings()

    def get_ai_system_settings_text(self, ai_id: str) -> str:
        return self.get_ai_system_settings(ai_id).get_text()

    def set_ai_system_settings_text(self, ai_id: str, text: str) -> None:
        return self.get_ai_system_settings(ai_id).set_text(text)

    def search_config_dir(self) -> str:
        dir_path_list = [
            ".",
            f"./{self.USER_DATA_DIR_NAME}/",
            f"../{self.USER_DATA_DIR_NAME}/",
            f"../../{self.USER_DATA_DIR_NAME}/",
            f"../../../{self.USER_DATA_DIR_NAME}/",
            f"./{self.SAMPLE_DIR_NAME}/{self.USER_DATA_DIR_NAME}/",
            f"../{self.SAMPLE_DIR_NAME}/{self.USER_DATA_DIR_NAME}/",
            f"../../{self.SAMPLE_DIR_NAME}/{self.USER_DATA_DIR_NAME}/",
        ]
        for dir_path in dir_path_list:
            if os.path.exists(os.path.join(dir_path, self._CONFIG_FILE_NAME)):
                return dir_path
        raise FileNotFoundError(f"{self._CONFIG_FILE_NAME} not found.")

    def get_deepl_auth_key(self) -> str:
        return self._config["DeepL"][self.KEY_DEEPL_AUTH_KEY]

    def set_deepl_auth_key(self, value: str) -> None:
        self._config["DeepL"][self.KEY_DEEPL_AUTH_KEY] = value

    def get_openai_api_key(self) -> str:
        value = self._config["OpenAI"][self.KEY_OPENAI_API_KEY]
        return value

    def set_openai_api_key(self, value: str) -> None:
        self._config["OpenAI"][self.KEY_OPENAI_API_KEY] = value

    def get_obs_host(self) -> str:
        return self._config["OBS"][self.KEY_OBS_HOST]

    def set_obs_host(self, value: str) -> None:
        self._config["OBS"][self.KEY_OBS_HOST] = value

    def get_obs_port_no(self) -> int:
        return self._config["OBS"][self.KEY_OBS_PORT_NO]

    def set_obs_port_no(self, value: int) -> None:
        self._config["OBS"][self.KEY_OBS_PORT_NO] = value

    def get_obs_password(self) -> str:
        return self._config["OBS"][self.KEY_OBS_PASSWORD]

    def set_obs_password(self, value: str) -> None:
        self._config["OBS"][self.KEY_OBS_PASSWORD] = value

    def get_obs_user_utterance_source_name(self) -> str:
        return self._config["OBS"][self.KEY_OBS_USER_UTTERANCE_SOURCE_NAME]

    def set_obs_user_utterance_source_name(self, value: str) -> None:
        self._config["OBS"][self.KEY_OBS_USER_UTTERANCE_SOURCE_NAME] = value

    def get_obs_ai_utterance_source_name(self) -> str:
        return self._config["OBS"][self.KEY_OBS_AI_UTTERANCE_SOURCE_NAME]

    def set_obs_ai_utterance_source_name(self, value: str) -> None:
        self._config["OBS"][self.KEY_OBS_AI_UTTERANCE_SOURCE_NAME] = value

    def get_voicevox_host(self) -> str:
        return self._config["VOICEVOX"][self.KEY_VOICEVOX_HOST]

    def set_voicevox_host(self, value: str) -> None:
        self._config["VOICEVOX"][self.KEY_VOICEVOX_HOST] = value

    def get_voicevox_port_no(self) -> int:
        return self._config["VOICEVOX"][self.KEY_VOICEVOX_PORT_NO]

    def set_voicevox_port_no(self, value: int) -> None:
        self._config["VOICEVOX"][self.KEY_VOICEVOX_PORT_NO] = value

    def get_voicevox_speaker_no(self) -> int:
        return self._config["VOICEVOX"][self.KEY_VOICEVOX_SPEAKER_NO]

    def set_voicevox_speaker_no(self, value: int) -> None:
        self._config["VOICEVOX"][self.KEY_VOICEVOX_SPEAKER_NO] = value

    def get_gcp_youtube_data_api_key(self) -> str:
        return self._config["YouTube"][self.KEY_GCP_YOUTUBE_DATA_API_KEY]

    def set_gcp_youtube_data_api_key(self, value: str) -> None:
        self._config["YouTube"][self.KEY_GCP_YOUTUBE_DATA_API_KEY] = value

    def get_youtube_live_url(self) -> str:
        return self._config["YouTube"][self.KEY_YOUTUBE_LIVE_URL]

    def set_youtube_live_url(self, value: str) -> None:
        self._config["YouTube"][self.KEY_YOUTUBE_LIVE_URL] = value

    def get_gcp_text_to_speech_api_key(self) -> str:
        return self._config["GoogleTextToSpeech"][self.KEY_GCP_TEXT_TO_SPEECH_API_KEY]

    def set_gcp_text_to_speech_api_key(self, value: str) -> None:
        self._config["GoogleTextToSpeech"][self.KEY_GCP_TEXT_TO_SPEECH_API_KEY] = value

    def get_gcp_text_to_speech_speaker_name(self) -> str:
        return self._config["GoogleTextToSpeech"][self.KEY_GCP_TEXT_TO_SPEECH_SPEAKER_NAME]

    def set_gcp_text_to_speech_speaker_name(self, value: str) -> None:
        self._config["GoogleTextToSpeech"][self.KEY_GCP_TEXT_TO_SPEECH_SPEAKER_NAME] = value

    def get_gcp_speech_to_text_api_key(self):
        return self._config["GoogleSpeechToText"][self.KEY_GCP_SPEECH_TO_TEXT_API_KEY]

    def set_gcp_speech_to_text_api_key(self, value: str) -> None:
        self._config["GoogleSpeechToText"][self.KEY_GCP_SPEECH_TO_TEXT_API_KEY] = value

    def get_pyaudio_secondary_output_enabled(self) -> bool:
        return self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED]

    def set_pyaudio_secondary_output_enabled(self, value: bool) -> None:
        self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED] = value

    def get_pyaudio_secondary_output_api_name(self) -> str:
        return self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_API_NAME]

    def set_pyaudio_secondary_output_api_name(self, value: str) -> None:
        self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_API_NAME] = value

    def get_pyaudio_secondary_output_device_name(self) -> str:
        return self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_DEVICE_NAME]

    def set_pyaudio_secondary_output_device_name(self, value: str) -> None:
        self._config["PyAudio"][self.KEY_PYAUDIO_SECONDARY_OUTPUT_DEVICE_NAME] = value

    def clone(self):
        return copy.deepcopy(self)

    def get_common_base_function_name(self) -> str:
        key = self.get_common_base_function()
        return self.base_function_dict[key.value]

    def get_common_base_function(self) -> BaseFunction:
        value = self._config["Common"][self.KEY_COMMON_BASE_FUNCTION]
        return BaseFunction.str2function(value)

    def set_common_base_function(self, function: BaseFunction) -> None:
        self._config["Common"][self.KEY_COMMON_BASE_FUNCTION] = function.value

    def get_common_input_function_name(self) -> str:
        key = self.get_common_input_function()
        return self.input_function_dict[key.value]

    def get_common_input_function(self) -> InputFunction:
        value = self._config["Common"][self.KEY_COMMON_INPUT_FUNCTION]
        return InputFunction.str2function(value)

    def set_common_input_function(self, function: InputFunction) -> None:
        self._config["Common"][self.KEY_COMMON_INPUT_FUNCTION] = function.value

    def get_common_output_function_name(self) -> str:
        function = self.get_common_output_function()
        return self.output_function_dict[function.value]

    def get_common_output_function(self) -> OutputFunction:
        value = self._config["Common"][self.KEY_COMMON_OUTPUT_FUNCTION]
        return OutputFunction.str2function(value)

    def set_common_output_function(self, function: OutputFunction) -> None:
        self._config["Common"][self.KEY_COMMON_OUTPUT_FUNCTION] = function.value

    def get_common_obs_enabled(self) -> bool:
        return self._config["Common"][self.KEY_COMMON_OBS_ENABLED]

    def set_common_obs_enabled(self, value: bool) -> None:
        self._config["Common"][self.KEY_COMMON_OBS_ENABLED] = value

    def get_common_v_magic_mirror_connection_enabled(self) -> bool:
        return self._config["Common"][self.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED]

    def set_common_v_magic_mirror_connection_enabled(self, value: bool) -> None:
        self._config["Common"][self.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED] = value

    def get_gui_app_title(self) -> str:
        return self._config["GUI"][self.KEY_GUI_APP_TITLE]

    def set_gui_app_title(self, value: str) -> None:
        self._config["GUI"][self.KEY_GUI_APP_TITLE] = value

    def get_gui_theme_name(self) -> str:
        return self._config["GUI"][self.KEY_GUI_THEME_NAME]

    def set_gui_theme_name(self, value: str) -> None:
        self._config["GUI"][self.KEY_GUI_THEME_NAME] = value

    def get_wrime_emotion_server_host(self) -> str:
        return self._config["WrimeEmotionServer"][self.KEY_WRIME_EMOTION_SERVER_HOST]

    def set_wrime_emotion_server_host(self, value: str) -> None:
        self._config["WrimeEmotionServer"][self.KEY_WRIME_EMOTION_SERVER_HOST] = value

    def get_wrime_emotion_server_port_no(self) -> int:
        return self._config["WrimeEmotionServer"][self.KEY_WRIME_EMOTION_SERVER_PORT_NO]

    def set_wrime_emotion_server_port_no(self, value: int) -> None:
        self._config["WrimeEmotionServer"][self.KEY_WRIME_EMOTION_SERVER_PORT_NO] = value

    def get_advanced_console_log_level(self) -> str:
        return self._config["Advanced"][self.KEY_ADVANCED_CONSOLE_LOG_LEVEL]

    def set_advanced_console_log_level(self, value: str) -> None:
        self._config["Advanced"][self.KEY_ADVANCED_CONSOLE_LOG_LEVEL] = value

    def get_advanced_chat_gpt_history_log_enabled(self) -> bool:
        return self._config["Advanced"][self.KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED]

    def set_advanced_chat_gpt_history_log_enabled(self, value: bool) -> None:
        self._config["Advanced"][self.KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED] = value

    def get_advanced_langchain_enabled(self) -> bool:
        return self._config["Advanced"][self.KEY_ADVANCED_LANGCHAIN_ENABLED]

    def set_advanced_langchain_enabled(self, value: bool) -> None:
        self._config["Advanced"][self.KEY_ADVANCED_LANGCHAIN_ENABLED] = value

    # langchain_conversation_verbose
    def get_langchain_conversation_verbose(self) -> bool:
        return self._config["LangChain"][self.KEY_LANGCHAIN_CONVERSATION_VERBOSE]

    def set_langchain_conversation_verbose(self, value: bool) -> None:
        self._config["LangChain"][self.KEY_LANGCHAIN_CONVERSATION_VERBOSE] = value

    def get_langchain_memory_type(self) -> LangChainMemoryType:
        result = self._config["LangChain"][self.KEY_LANGCHAIN_MEMORY_TYPE]
        return LangChainMemoryType.name2memory_type(result)

    def set_langchain_memory_type(self, memory_type: LangChainMemoryType) -> None:
        self._config["LangChain"][self.KEY_LANGCHAIN_MEMORY_TYPE] = memory_type.name
