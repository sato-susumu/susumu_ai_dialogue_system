import time
from dataclasses import dataclass

from google.cloud import texttospeech
from loguru import logger

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.base_tts import BaseTTS


@dataclass
class GoogleCloudTTSSpeaker:
    display_name: str
    speaker_name: str


# noinspection PyPackageRequirements
class GoogleCloudTTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)
        # noinspection PyBroadException
        try:
            self.client = texttospeech.TextToSpeechClient()
        except Exception:
            # 認証に失敗した場合は、APIキーでリトライ
            api_key = self._config.get_gcp_text_to_speech_api_key()
            self.client = texttospeech.TextToSpeechClient(client_options={"api_key": api_key})

    def tts_play_sync(self, text: str) -> None:
        super().tts_play_sync(text)
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        self._start_event_publish()
        self._wav_play_sync(audio_content, self._on_playback_completed, self._on_error)

    def tts_play_async(self, text: str) -> None:
        super().tts_play_async(text)
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        self._start_event_publish()
        self._wav_play_async(audio_content, self._on_playback_completed, self._on_error)

    def _on_playback_completed(self):
        self._end_event_publish()

    def _on_error(self, e: Exception):
        self._error_event_publish(e)

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        audio_content = self._tts(text, texttospeech.AudioEncoding.MP3)
        with open(file_path, "wb") as out:
            out.write(audio_content)

    def tts_save_wav(self, text: str, file_path: str) -> None:
        audio_content = self._tts(text, texttospeech.AudioEncoding.LINEAR16)
        with open(file_path, "wb") as out:
            out.write(audio_content)

    # noinspection PyMethodMayBeStatic
    def _speaker_name_to_language_code(self, speaker_name: str) -> str:
        return speaker_name.split("-")[0] + "-" + speaker_name.split("-")[1]

    # 型の不一致はあとまわし
    # noinspection PyTypeChecker
    def _tts(self, text: str, format_name: texttospeech.AudioEncoding) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        speaker_name = self._config.get_gcp_text_to_speech_speaker_name()
        language_code = self._speaker_name_to_language_code(speaker_name)

        voice = texttospeech.VoiceSelectionParams(
            name=speaker_name,
            language_code=language_code,
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

        before = time.perf_counter()
        response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        after = time.perf_counter()
        logger.debug(f"GoogleCloudTTS processing time={after - before:.3f} s")
        return response.audio_content

    _sort_priority_order = ["ja-JP", "en-US"]

    def _get_priority(self, item: GoogleCloudTTSSpeaker) -> int:
        lang_code = item.display_name[:5]
        if lang_code in self._sort_priority_order:
            return self._sort_priority_order.index(lang_code)
        else:
            return len(self._sort_priority_order)

    def _sort_speaker(self, speakers: list[GoogleCloudTTSSpeaker]) -> list[GoogleCloudTTSSpeaker]:
        sorted_list = sorted(speakers, key=self._get_priority)
        sorted_list += [x for x in speakers if x not in sorted_list]
        return sorted_list

    def get_speakers(self) -> list[GoogleCloudTTSSpeaker]:
        voices = self.client.list_voices()
        speakers: list[GoogleCloudTTSSpeaker] = []

        for voice in voices.voices:
            ssml_gender = voice.ssml_gender
            gender = "MALE" if ssml_gender.value == 1 else "FEMALE"
            name = voice.name
            speakers.append(GoogleCloudTTSSpeaker(f"{name}-{gender}", f"{name}"))

        return self._sort_speaker(speakers)


if __name__ == '__main__':
    from susumu_ai_dialogue_system.infrastructure.config import Config
    from pprint import pprint

    _config = Config()
    _config.search_and_load()
    _tts = GoogleCloudTTS(_config)
    _speakers = _tts.get_speakers()
    pprint(_speakers)
