from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.pyaudio_player import PyAudioPlayer


# noinspection PyMethodMayBeStatic
class BaseTTS:
    def __init__(self, config: Config):
        self._config = config
        self._player = PyAudioPlayer(config)

    def tts_play(self, text: str) -> None:
        pass

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass

    def _wav_play(self, audio_content: bytes) -> None:
        self._player.play_bytes_sync(audio_content)
