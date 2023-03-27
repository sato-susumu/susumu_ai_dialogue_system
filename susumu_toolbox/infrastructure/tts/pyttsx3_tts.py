import pyttsx3

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.tts.base_tts import BaseTTS


class Pyttsx3TTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)
        self.engine = pyttsx3.init()

    def tts_play_sync(self, text: str) -> None:
        super().tts_play_sync(text)
        self._play_sync(text)

    def tts_play_async(self, text: str) -> None:
        super().tts_play_async(text)
        # 非同期再生に対応していないため、同期再生
        self._play_sync(text)

    def _play_sync(self, text: str) -> None:
        self._start_event_publish()
        self.engine.say(text)
        self.engine.runAndWait()
        self._end_event_publish()

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass
