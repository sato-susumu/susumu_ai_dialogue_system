import json

import requests

from susumu_toolbox.tts.base_tts import BaseTTS


# noinspection PyMethodMayBeStatic,HttpUrlsUsage
class VoicevoxTTS(BaseTTS):
    def __init__(self, speaker: int = 8, host: str = '127.0.0.1'):
        super().__init__()
        # server_addrは"localhost"だと遅いことがあるので注意
        self._host = host
        self._speaker = speaker

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
        response = requests.get(f"http://{self._host}:50021/version")
        return response.text.replace("\"", "")

    def get_speakers(self) -> dict:
        response_json = requests.get(f"http://{self._host}:50021/speakers").json()
        speakers = {}
        for item in response_json:
            speakers[item["name"]] = {}
            for style in item["styles"]:
                speakers[item["name"]][style["name"]] = style["id"]
        return speakers

    def _synthesize(self, text: str) -> bytes:
        # before = perf_counter()
        query_json = requests.post(f"http://{self._host}:50021/audio_query",
                                   params={'text': text, 'speaker': self._speaker}).json()
        query_json["speedScale"] = 1.2
        query_json["pitchScale"] = 0

        response = requests.post(f"http://{self._host}:50021/synthesis",
                                 params={'speaker': self._speaker},
                                 data=json.dumps(query_json))
        # TODO: 何らかの実装でパフォーマンス測定
        # after = perf_counter()
        # self._latest_performance_metrics = f"{after - before:.3f} s"
        return response.content
