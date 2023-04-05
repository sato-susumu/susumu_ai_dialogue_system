from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.base_tts import BaseTTS


# noinspection PyMethodMayBeStatic
class GttsTTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)

    def tts_play_sync(self, text: str) -> None:
        super().tts_play_sync(text)
        if text == "":
            return
        self._play_sync(text)

    def tts_play_async(self, text: str) -> None:
        super().tts_play_async(text)
        if text == "":
            return
        # 非同期再生に対応していないため、同期再生
        self._play_sync(text)

    def _play_sync(self, text: str) -> None:
        self._start_event_publish()
        fp = BytesIO()
        gTTS(text=text, lang='ja').write_to_fp(fp)
        fp.seek(0)

        # 速度を上げて再生
        af = AudioSegment.from_file(fp, format="mp3").speedup(playback_speed=1.5)
        play(af)
        self._end_event_publish()

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        # tts_playと違って等倍速で保存
        # おまけ機能なので、今のところ改良予定なし
        gTTS(text=text, lang='ja').save(file_path)

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass
