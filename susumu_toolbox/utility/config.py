import os
from typing import Optional

from omegaconf import OmegaConf


# noinspection PyMethodMayBeStatic
class Config:
    CONFIG_FILE_NAME = "config.yaml"
    KEY_OPENAI_API_KEY = "openai_api_key"

    def __init__(self):
        # 辞書からコンフィグを読み込む
        default_yaml = """
            DeepL:
              deepl_auth_key: "DEEPLの認証キー"
            OpenAI:
              openai_api_key: "OpenAIのAPIキー"
            OBS:
              obs_host: "127.0.0.1"
              obs_port_no: 4444
              obs_password: "パスワード"
            VOICEVOX:
              voicevox_host: "127.0.0.1"
              voicevox_prot_no: 50021
              voicevox_speaker_no: 8
            ParlAI:
              parlai_host: "127.0.0.1"
              parlai_prot_no: 35496
            YouTube:
              # YouTube Data API v3のAPIキー
              youtube_api_key: ""
              # YouTubeのライブ配信URL。例：https://www.youtube.com/watch?v=xxxxxxxxxxx
              youtube_live_url: ""
            PyAudio:
              # 標準スピーカー以外にも同時出力するかどうか
              pyaudio_second_output_enabled: false
              # 名前の一部でもいい
              pyaudio_second_output_host_api_name: "MME"
              pyaudio_second_output_device_name: "VB-Audio Virtual C"        
        """
        self._config = OmegaConf.create(default_yaml)

        # TODO: 下記のようにコンフィグファイルパスの扱いはごちゃっとしているので整理する
        # 自動検知もしくはload時に引数で指定されたコンフィグファイルパス
        # 次のようなケースもある
        # ・自動検知で見つかり、そのパスを使う。ファイルは存在する
        # ・load時に引数で指定されたもののファイルが存在しない
        # ・自動検知で見つからず、仮のパスを使う。ファイルは存在しない
        self._current_config_path = self._get_config_file_path()

    def _get_config_file_path(self) -> str:
        return os.path.join(self.get_config_dir(), self.CONFIG_FILE_NAME)

    def exist_config_file(self, file_path) -> bool:
        return os.path.exists(file_path)

    def save(self) -> None:
        OmegaConf.save(self._config, self._current_config_path)

    # noinspection DuplicatedCode
    def load(self, file_path: Optional[str] = None) -> None:
        if file_path is None:
            file_path = self._get_config_file_path()
        if self.exist_config_file(file_path):
            loaded_config = OmegaConf.load(file_path)
            self._config = OmegaConf.merge(self._config, loaded_config)
        self._current_config_path = file_path

    def get_config_dir(self) -> str:
        # カレントフォルダ用
        if os.path.exists(self.CONFIG_FILE_NAME):
            return "."
        # ルートフォルダ用
        # TODO:__file__の撤廃
        path = os.path.join(os.path.dirname(__file__), "../config/")
        if os.path.exists(path):
            return path
        # サンプルフォルダ用
        # TODO:__file__の撤廃
        path = os.path.join(os.path.dirname(__file__), "../../config/")
        if os.path.exists(path):
            return path
        return "."

    def get_deepl_auth_key(self) -> str:
        return self._config["DeepL"]["deepl_auth_key"]

    def get_openai_api_key(self) -> str:
        value = self._config["OpenAI"][self.KEY_OPENAI_API_KEY]
        return value

    def set_openai_api_key(self, value):
        self._config["OpenAI"][self.KEY_OPENAI_API_KEY] = value

    def get_obs_host(self):
        return self._config["OBS"]["obs_host"]

    def get_obs_port_no(self):
        return self._config["OBS"]["obs_port_no"]

    def get_obs_password(self):
        return self._config["OBS"]["obs_password"]

    def get_voicevox_host(self):
        return self._config["VOICEVOX"]["voicevox_host"]

    def get_voicevox_port_no(self):
        return self._config["VOICEVOX"]["voicevox_prot_no"]

    def get_voicevox_speaker_no(self):
        return self._config["VOICEVOX"]["voicevox_speaker_no"]

    def get_parlai_host(self):
        return self._config["ParlAI"]["parlai_host"]

    def get_parlai_port_no(self):
        return self._config["ParlAI"]["parlai_prot_no"]

    def get_youtube_api_key(self):
        return self._config["YouTube"]["youtube_api_key"]

    def get_youtube_live_url(self):
        return self._config["YouTube"]["youtube_live_url"]

    def get_pyaudio_second_output_enabled(self):
        return self._config["PyAudio"]["pyaudio_second_output_enabled"]

    def get_pyaudio_second_output_host_api_name(self):
        return self._config["PyAudio"]["pyaudio_second_output_host_api_name"]

    def get_pyaudio_second_output_device_name(self):
        return self._config["PyAudio"]["pyaudio_second_output_device_name"]
