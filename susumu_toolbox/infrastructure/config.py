import copy
import os
from typing import List, Any

from omegaconf import OmegaConf


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
    KEY_OBS_SCENE_NAME = "obs_scene_name"
    KEY_OBS_USER_UTTERANCE_SOURCE_NAME = "obs_user_utterance_source_name"
    KEY_OBS_AI_UTTERANCE_SOURCE_NAME = "obs_ai_utterance_source_name"
    KEY_YOUTUBE_LIVE_URL = "youtube_live_url"
    KEY_GCP_YOUTUBE_DATA_API_KEY = "gcp_youtube_data_api_key"
    KEY_COMMON_BASE_FUNCTION = "common_base_function"
    KEY_COMMON_CHAT_FUNCTION = "common_chat_function"
    KEY_COMMON_INPUT_FUNCTION = "common_input_function"
    KEY_COMMON_OUTPUT_FUNCTION = "common_output_function"
    KEY_COMMON_OBS_ENABLED = "common_obs_enabled"
    KEY_PARLAI_HOST = "parlai_host"
    KEY_PARLAI_PORT_NO = "parlai_port_no"
    KEY_GCP_TEXT_TO_SPEECH_API_KEY = "gcp_text_to_speech_api_key"
    KEY_GCP_SPEECH_TO_TEXT_API_KEY = "gcp_speech_to_text_api_key"
    KEY_GUI_APP_TITLE = "gui_app_title"
    KEY_GUI_THEME_NAME = "gui_theme_name"

    BASE_FUNCTION_VOICE_DIALOGUE = "voice_dialogue"
    BASE_FUNCTION_TEXT_DIALOGUE = "text_dialogue"
    BASE_FUNCTION_AI_TUBER = "ai_tuber"

    INPUT_FUNCTION_BASE = "base_stt"
    INPUT_FUNCTION_SR_GOOGLE = "sr_google"
    INPUT_FUNCTION_STDIN_PSEUD = "stdin_pseud"
    INPUT_FUNCTION_GOOGLE_STREAMING = "google_streaming"
    INPUT_FUNCTION_YOUTUBE_PSEUD = "youtube_pseud"
    INPUT_FUNCTION_WHISPER_API = "whisper_api"

    CHAT_FUNCTION_CHATGPT = "chatgpt"
    CHAT_FUNCTION_PARLAI = "parlai"

    OUTPUT_FUNCTION_BASE = "base_tts"
    OUTPUT_FUNCTION_NONE = "none"
    OUTPUT_FUNCTION_PYTTSX3 = "pyttsx3"
    OUTPUT_FUNCTION_VOICEVOX = "voicevox"
    OUTPUT_FUNCTION_GOOGLE_CLOUD = "google_cloud"
    OUTPUT_FUNCTION_GTTS = "gtts"

    USER_DATA_DIR_NAME = "user_data"
    SAMPLE_DIR_NAME = "application"

    base_function_dict = {
        BASE_FUNCTION_VOICE_DIALOGUE: "音声対話",
        BASE_FUNCTION_AI_TUBER: "AITuber",
        BASE_FUNCTION_TEXT_DIALOGUE: "文字対話",
    }
    input_function_dict = {
        INPUT_FUNCTION_SR_GOOGLE: "サンプル音声認識",
        INPUT_FUNCTION_STDIN_PSEUD: "文字入力",
        INPUT_FUNCTION_GOOGLE_STREAMING: "Google Speech-to-Text ストリーミング音声認識 (追加設定が必要)",
        INPUT_FUNCTION_WHISPER_API: "Whisper API音声認識 (OpenAI API Key設定が必要)",
        INPUT_FUNCTION_YOUTUBE_PSEUD: "YouTubeコメント取得 (追加設定が必要)",
    }
    chat_function_dict = {
        CHAT_FUNCTION_CHATGPT: "ChatGPT API (OpenAI API Key設定が必要)",
        CHAT_FUNCTION_PARLAI: "ParlAIクライント (追加設定が必要)",
    }
    output_function_dict = {
        OUTPUT_FUNCTION_NONE: "なし",
        OUTPUT_FUNCTION_PYTTSX3: "サンプル音声合成 pyttsx3",
        OUTPUT_FUNCTION_VOICEVOX: "VOICEVOX (VOICEVOXアプリ起動が必要)",
        OUTPUT_FUNCTION_GOOGLE_CLOUD: "Google Text-to-Speech (追加設定が必要)",
        OUTPUT_FUNCTION_GTTS: "サンプル音声合成 gTTS",
    }

    def __init__(self):
        # 仕方なくここでimport
        from susumu_toolbox.infrastructure.ai_config_list import AiConfigList
        # 辞書からコンフィグを読み込む
        default_yaml = """
            Common:
              format_version: 1
              common_base_function: "voice_dialogue"
              common_input_function: "sr_google"
              common_chat_function: "chatgpt"
              common_output_function: "pyttsx3"
              common_obs_enabled: false
            DeepL:
              deepl_auth_key: ""
            OpenAI:
              openai_api_key: ""
            OBS:
              obs_host: "127.0.0.1"
              obs_port_no: 4444
              obs_password: "パスワード"
              obs_scene_name: "scene1"
              obs_user_utterance_source_name: "user_input_text"
              obs_ai_utterance_source_name: "ai_output_text"
            VOICEVOX:
              voicevox_host: "127.0.0.1"
              voicevox_port_no: 50021
              voicevox_speaker_no: 8
            ParlAI:
              parlai_host: "127.0.0.1"
              parlai_port_no: 35496
            YouTube:
              # GCP YouTube Data API v3のAPIキー
              gcp_youtube_data_api_key: ""
              # YouTubeのライブ配信URL。例：https://www.youtube.com/watch?v=xxxxxxxxxxx
              youtube_live_url: ""
            GoogleTextToSpeech:
              gcp_text_to_speech_api_key:
            GoogleSpeechToText:
              gcp_speech_to_text_api_key:
            PyAudio:
              # 標準スピーカー以外にも同時出力するかどうか
              pyaudio_second_output_enabled: false
              # 名前の一部でもいい
              pyaudio_second_output_host_api_name: "MME"
              pyaudio_second_output_device_name: "VB-Audio Virtual C"
            GUI:
              gui_app_title: "susumu_toolbox"
              gui_theme_name: "Bright Colors"   
        """
        self._config = OmegaConf.create(default_yaml)
        # 設定ファイルのパス。初回保存前だとファイルが存在しないこともあるので注意
        self._current_config_path = None
        self._ai_config_list = AiConfigList(self)

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

    def make_ai_config_dir_if_needed(self) -> None:
        dir_path = self.get_user_data_dir_path()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_ai_id_list(self) -> List[str]:
        return self._ai_config_list.get_ai_id_list()

    def get_ai_system_settings(self, ai_id: str) -> Any:
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

    def get_obs_scene_name(self) -> str:
        return self._config["OBS"][self.KEY_OBS_SCENE_NAME]

    def set_obs_scene_name(self, value: str) -> None:
        self._config["OBS"][self.KEY_OBS_SCENE_NAME] = value

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

    def get_parlai_host(self) -> str:
        return self._config["ParlAI"][self.KEY_PARLAI_HOST]

    def set_parlai_host(self, value: str) -> None:
        self._config["ParlAI"][self.KEY_PARLAI_HOST] = value

    def get_parlai_port_no(self) -> int:
        return self._config["ParlAI"][self.KEY_PARLAI_PORT_NO]

    def set_parlai_port_no(self, value: int) -> None:
        self._config["ParlAI"][self.KEY_PARLAI_PORT_NO] = value

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

    def get_gcp_speech_to_text_api_key(self):
        return self._config["GoogleSpeechToText"][self.KEY_GCP_SPEECH_TO_TEXT_API_KEY]

    def set_gcp_speech_to_text_api_key(self, value: str) -> None:
        self._config["GoogleSpeechToText"][self.KEY_GCP_SPEECH_TO_TEXT_API_KEY] = value

    def get_pyaudio_second_output_enabled(self) -> bool:
        return self._config["PyAudio"]["pyaudio_second_output_enabled"]

    def get_pyaudio_second_output_host_api_name(self) -> str:
        return self._config["PyAudio"]["pyaudio_second_output_host_api_name"]

    def get_pyaudio_second_output_device_name(self) -> str:
        return self._config["PyAudio"]["pyaudio_second_output_device_name"]

    def clone(self):
        return copy.deepcopy(self)

    def get_common_base_function_name(self) -> str:
        key = self.get_common_base_function_key()
        return self.base_function_dict[key]

    def get_common_base_function_key(self) -> str:
        return self._config["Common"][self.KEY_COMMON_BASE_FUNCTION]

    def set_common_base_function_key(self, value: str) -> None:
        self._config["Common"][self.KEY_COMMON_BASE_FUNCTION] = value

    def get_common_input_function_name(self) -> str:
        key = self.get_common_input_function_key()
        return self.input_function_dict[key]

    def get_common_input_function_key(self) -> str:
        return self._config["Common"][self.KEY_COMMON_INPUT_FUNCTION]

    def set_common_input_function_key(self, value: str) -> None:
        self._config["Common"][self.KEY_COMMON_INPUT_FUNCTION] = value

    def get_common_chat_function_name(self) -> str:
        key = self.get_common_chat_function_key()
        return self.chat_function_dict[key]

    def get_common_chat_function_key(self) -> str:
        return self._config["Common"][self.KEY_COMMON_CHAT_FUNCTION]

    def set_common_chat_function_key(self, value: str) -> None:
        self._config["Common"][self.KEY_COMMON_CHAT_FUNCTION] = value

    def get_common_output_function_name(self) -> str:
        key = self.get_common_output_function_key()
        return self.output_function_dict[key]

    def get_common_output_function_key(self) -> str:
        return self._config["Common"][self.KEY_COMMON_OUTPUT_FUNCTION]

    def set_common_output_function_key(self, value: str) -> None:
        self._config["Common"][self.KEY_COMMON_OUTPUT_FUNCTION] = value

    def get_common_obs_enabled(self) -> bool:
        return self._config["Common"][self.KEY_COMMON_OBS_ENABLED]

    def set_common_obs_enabled(self, value: bool) -> None:
        self._config["Common"][self.KEY_COMMON_OBS_ENABLED] = value

    def get_gui_app_title(self) -> str:
        return self._config["GUI"][self.KEY_GUI_APP_TITLE]

    def get_gui_theme_name(self) -> str:
        return self._config["GUI"][self.KEY_GUI_THEME_NAME]
