import io
import threading
import wave

import pyaudio

from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.pyaudio_utility import PyAudioUtility


# noinspection PyMethodMayBeStatic
class PyAudioPlayer:
    def __init__(self, config: Config):
        self._thread2 = None
        self._thread1 = None
        self._config = config
        # 複数スレッドで同時にPyAudioを取得するとうまく動作しなかったっぽいので、1箇所のみで取得
        self._pa = pyaudio.PyAudio()
        self._stop_event = threading.Event()

    def _get_second_output_device_id(self) -> int:
        second_output_enabled = self._config.get_pyaudio_second_output_enabled()
        if not second_output_enabled:
            return -1
        # 指定されたデバイスのデバイスID取得
        # 見つからない場合は-1
        second_output_device_id = PyAudioUtility().get_speaker_id(
            self._config.get_pyaudio_second_output_host_api_name(),
            self._config.get_pyaudio_second_output_device_name()
        )
        return second_output_device_id

    def _play_bytes(self, audio_content: bytes, output_no: int, output_device_id) -> None:
        wf = None
        stream = None
        try:
            wf = wave.open(io.BytesIO(audio_content), 'rb')
            if output_no == 0:
                stream = self._pa.open(
                    format=pyaudio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True
                )
            elif output_no == 1:
                if output_device_id != -1:
                    stream = self._pa.open(
                        format=pyaudio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=output_device_id
                    )
                else:
                    return
            else:
                return
            chunk_size = 1024
            data = wf.readframes(chunk_size)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(chunk_size)
                if self._stop_event.is_set():
                    break
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            if wf:
                wf.close()

    def play_bytes_sync(self, audio_content: bytes) -> None:
        second_output_device_id = self._get_second_output_device_id()
        self._thread1 = threading.Thread(target=self._play_bytes, args=(audio_content, 0, 0))
        self._thread2 = threading.Thread(target=self._play_bytes, args=(audio_content, 1, second_output_device_id))

        self._stop_event.clear()

        self._thread1.start()
        self._thread2.start()
        self._thread1.join()
        self._thread2.join()

    def play_wav_file(self, file_path: str):
        with open(file_path, 'rb') as wf:
            data = wf.read()
        self.play_bytes_sync(data)

    def stop(self):
        if self._thread1 or self._thread2:
            self._stop_event.set()
            self._thread1.join()
            self._thread2.join()
            self._thread1 = None
            self._thread2 = None


if __name__ == "__main__":
    _config = Config()
    _config.load()
    player = PyAudioPlayer(_config)
    player.play_wav_file("test.wav")
