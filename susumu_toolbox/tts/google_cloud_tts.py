# あとまわし
# noinspection PyPackageRequirements
from google.cloud import texttospeech

from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.utility.config import Config


class GoogleCloudTTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)
        self.client = texttospeech.TextToSpeechClient()

    def tts_play_sync(self, text: str) -> None:
        super().tts_play_sync(text)
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        self._wav_play_sync(audio_content)

    def tts_play_async(self, text: str) -> None:
        super().tts_play_async(text)
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        self._wav_play_async(audio_content)

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        audio_content = self._tts(text, texttospeech.AudioEncoding.MP3)
        with open(file_path, "wb") as out:
            out.write(audio_content)

    def tts_save_wav(self, text: str, file_path: str) -> None:
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        with open(file_path, "wb") as out:
            out.write(audio_content)

    # 型の不一致はあとまわし
    # noinspection PyTypeChecker
    def _tts(self, text: str, format_name: texttospeech.AudioEncoding) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            name='ja-JP-Neural2-B',
            language_code="ja-JP",
            ssml_gender=texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=format_name,
            # 読み上げ速度 (0.25～4.0)
            speaking_rate=1.25,
            # ピッチ (-20.0～20.0)
            pitch=0,
            # ゲイン (-96.0～16.0)。-6で半分。6で2倍。10以下を推奨
            volume_gain_db=0.0,
            # 他にもオプションあり
        )

        # TODO: 何らかの実装でパフォーマンス測定
        # start = time.perf_counter()
        response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        # print(time.perf_counter() - start)
        return response.audio_content
