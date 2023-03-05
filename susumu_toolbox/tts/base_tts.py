import io
import wave

import pyaudio

from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.pyaudio_utility import PyAudioUtility


# noinspection PyMethodMayBeStatic
class BaseTTS:
    def __init__(self, config: Config):
        self._config = config

    def tts_play(self, text: str) -> None:
        pass

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass

    def _get_second_output_device_id(self) -> int:
        second_output_enabled = self._config.get_base_tts_second_output_enabled()
        if not second_output_enabled:
            return -1
        # 指定されたデバイスのデバイスID取得
        # 見つからない場合は-1
        second_output_device_id = PyAudioUtility().get_speaker_id(
            self._config.get_base_tts_second_output_host_api_name(),
            self._config.get_base_tts_second_output_device_name()
        )
        return second_output_device_id

    def _wav_play(self, audio_content: bytes) -> None:
        second_output_device_id = self._get_second_output_device_id()
        wf = None
        pa = None
        stream1 = None
        stream2 = None
        try:
            wf = wave.open(io.BytesIO(audio_content), 'rb')
            pa = pyaudio.PyAudio()
            stream1 = pa.open(
                format=pyaudio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            if second_output_device_id != -1:
                stream2 = pa.open(
                    format=pyaudio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=second_output_device_id
                )
            chunk_size = 1024
            data = wf.readframes(chunk_size)
            while len(data) > 0:
                stream1.write(data)
                if stream2:
                    stream2.write(data)
                data = wf.readframes(chunk_size)
        finally:
            if stream1:
                stream1.stop_stream()
                stream1.close()
            if stream2:
                stream2.stop_stream()
                stream2.close()
            if pa:
                pa.terminate()
            if wf:
                wf.close()
