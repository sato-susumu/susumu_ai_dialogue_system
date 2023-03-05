import json

import requests

from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,HttpUrlsUsage
class VoicevoxTTS(BaseTTS):
    def __init__(self, config: Config):
        super().__init__(config)

    def tts_play(self, text: str) -> None:
        audio_content = self._synthesize(text)
        self._wav_play(audio_content)

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
        return response.text.replace("\"", "")

    def get_speakers(self) -> dict:
        host = self._config.get_voicevox_host()
        port_no = self._config.get_voicevox_port_no()
        response_json = requests.get(f"http://{host}:{port_no}/speakers").json()
        speakers = {}
        for item in response_json:
            speakers[item["name"]] = {}
            for style in item["styles"]:
                speakers[item["name"]][style["name"]] = style["id"]
        return speakers

    def _synthesize(self, text: str) -> bytes:
        # before = perf_counter()
        host = self._config.get_voicevox_host()
        port_no = self._config.get_voicevox_port_no()
        speaker_no = self._config.get_voicevox_speaker_no()
        query_json = requests.post(f"http://{host}:{port_no}/audio_query",
                                   params={'text': text, 'speaker': speaker_no}).json()
        query_json["speedScale"] = 1.2
        query_json["pitchScale"] = 0

        response = requests.post(f"http://{host}:{port_no}/synthesis",
                                 params={'speaker': speaker_no},
                                 data=json.dumps(query_json))
        # TODO: 何らかの実装でパフォーマンス測定
        # after = perf_counter()
        # self._latest_performance_metrics = f"{after - before:.3f} s"
        return response.content
