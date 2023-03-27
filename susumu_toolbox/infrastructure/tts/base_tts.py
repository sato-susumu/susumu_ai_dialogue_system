from enum import Enum

from event_channel.threaded_event_channel import ThreadedEventChannel

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.pyaudio_player import PyAudioPlayer


class TTSEvent(Enum):
    # 音声合成(単発)の開始イベント
    START = "tts_start"
    # 音声合成(単発)の終了イベント
    END = "tts_end"
    # 音声合成(単発)のエラーイベント
    ERROR = "tts_error"


# noinspection PyMethodMayBeStatic
class BaseTTS:
    def __init__(self, config: Config):
        self._config = config
        self._player = PyAudioPlayer(config)
        self.__event_channel = ThreadedEventChannel(blocking=False)

    def event_subscribe(self, event_name: TTSEvent, func):
        self.__event_channel.subscribe(event_name.value, func)

    def _event_publish(self, event: TTSEvent, *args, **kwargs):
        self.__event_channel.publish(event.value, *args, **kwargs)

    def _start_event_publish(self):
        self._event_publish(TTSEvent.START)

    def _end_event_publish(self):
        self._event_publish(TTSEvent.END)

    def _error_event_publish(self, e: Exception):
        self._event_publish(TTSEvent.ERROR, e)

    def tts_play_sync(self, text: str) -> None:
        print(f"tts_play_sync() is called. text: {text}")

    def tts_play_async(self, text: str) -> None:
        print(f"tts_play_async() is called. text: {text}")

    def is_playing(self) -> bool:
        return self._player.is_playing()

    def tts_stop(self) -> None:
        self._player.stop()

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass

    def _wav_play_sync(self, audio_content: bytes, on_playback_completed, on_error) -> None:
        self._player.play_bytes_sync(audio_content, on_playback_completed, on_error)

    def _wav_play_async(self, audio_content: bytes, on_playback_completed, on_error) -> None:
        self._player.play_bytes_async(audio_content, on_playback_completed, on_error)
