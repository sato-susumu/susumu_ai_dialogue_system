import io
import wave

import pyaudio


# noinspection PyMethodMayBeStatic
class BaseTTS:
    def __init__(self):
        pass

    def tts_play(self, text: str) -> None:
        pass

    def tts_save_mp3(self, text: str, file_path: str) -> None:
        pass

    def tts_save_wav(self, text: str, file_path: str) -> None:
        pass

    def _wav_play(self, audio_content: bytes) -> None:
        wf = None
        pa = None
        stream = None
        try:
            wf = wave.open(io.BytesIO(audio_content), 'rb')
            pa = pyaudio.PyAudio()
            stream = pa.open(
                format=pyaudio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            chunk_size = 1024
            data = wf.readframes(chunk_size)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(chunk_size)
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            if pa:
                pa.terminate()
            if wf:
                wf.close()
