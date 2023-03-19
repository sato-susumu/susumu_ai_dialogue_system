from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.pyaudio_player import PyAudioPlayer


# noinspection PyMethodMayBeStatic
class BaseTTS:
    def __init__(self, config: Config):
        self._config = config
        self._player = PyAudioPlayer(config)

    def tts_play_sync(self, text: str) -> None:
        print(f"tts_play_sync() is called. text: {text}")
        pass

    def tts_play_async(self, text: str) -> None:
        print(f"tts_play_async() is called. text: {text}")
        pass

    def is_playing(self) -> bool:
        return self._player.is_playing()

    def tts_stop(self) -> None:
        self._player.stop()

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass

    def _wav_play_sync(self, audio_content: bytes) -> None:
        self._player.play_bytes_sync(audio_content)

    def _wav_play_async(self, audio_content: bytes) -> None:
        self._player.play_bytes_async(audio_content)
