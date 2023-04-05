import json

import loguru
import requests

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.base_tts import BaseTTS


# noinspection PyMethodMayBeStatic,HttpUrlsUsage
class VoicevoxTTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)

    def tts_play_sync(self, text: str) -> None:
        super().tts_play_sync(text)
        audio_content = self._synthesize(text)
        self._start_event_publish()
        self._wav_play_sync(audio_content, self._on_playback_completed, self._on_error)

    def tts_play_async(self, text: str) -> None:
        super().tts_play_async(text)
        audio_content = self._synthesize(text)
        self._start_event_publish()
        self._wav_play_async(audio_content, self._on_playback_completed, self._on_error)

    def _on_playback_completed(self):
        self._end_event_publish()

    def _on_error(self, e: Exception):
        self._error_event_publish(e)

    def tts_save_wav(self, text: str, file_path: str) -> None:
        audio_content = self._synthesize(text)
        self._save_wav(audio_content, file_path)

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def _save_wav(self, audio_content: bytes, filename: str) -> None:
        with open(filename, "wb") as out:
            out.write(audio_content)

    def get_version(self) -> str:
        host = self._config.get_voicevox_host()
        port_no = self._config.get_voicevox_port_no()
        response = requests.get(f"http://{host}:{port_no}/version")
        response.raise_for_status()
        return response.text.replace("\"", "")

    def get_raw_speakers(self) -> list:
        host = self._config.get_voicevox_host()
        port_no = self._config.get_voicevox_port_no()
        response = requests.get(f"http://{host}:{port_no}/speakers")
        response.raise_for_status()
        return response.json()

    def get_speakers(self) -> dict:
        json_list = self.get_raw_speakers()
        result = {}
        for entry in json_list:
            for style in entry['styles']:
                key = f"{entry['name']}-{style['name']}"
                result[key] = style['id']
        return result

    def _synthesize(self, text: str) -> bytes:
        # before = perf_counter()
        host = self._config.get_voicevox_host()
        port_no = self._config.get_voicevox_port_no()
        speaker_no = self._config.get_voicevox_speaker_no()
        response = requests.post(f"http://{host}:{port_no}/audio_query",
                                 params={'text': text, 'speaker': speaker_no})
        response.raise_for_status()
        query_json = response.json()

        query_json["speedScale"] = 1.2
        query_json["pitchScale"] = 0

        response = requests.post(f"http://{host}:{port_no}/synthesis",
                                 params={'speaker': speaker_no},
                                 data=json.dumps(query_json))
        # TODO: 何らかの実装でパフォーマンス測定
        # after = perf_counter()
        # self._latest_performance_metrics = f"{after - before:.3f} s"
        return response.content


if __name__ == "__main__":
    _config = Config()
    tts = VoicevoxTTS(_config)
    loguru.logger.debug(tts.get_version())
    loguru.logger.debug(tts.get_speakers())
