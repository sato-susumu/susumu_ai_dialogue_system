from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from susumu_toolbox.tts.base_tts import BaseTTS


class GttsTTS(BaseTTS):
    def __init__(self):
        super().__init__()

    def tts_play(self, text: str) -> None:
        fp = BytesIO()
        gTTS(text=text, lang='ja').write_to_fp(fp)
        fp.seek(0)

        # 速度を上げて再生
        af = AudioSegment.from_file(fp, format="mp3").speedup(playback_speed=1.5)
        play(af)

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        # tts_playと違って等倍速で保存
        # おまけ機能なので、今のところ改良予定なし
        gTTS(text=text, lang='ja').save(file_path)

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass
