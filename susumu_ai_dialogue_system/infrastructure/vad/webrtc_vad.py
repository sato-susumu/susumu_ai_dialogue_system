import loguru
import pyaudio
import webrtcvad

from susumu_ai_dialogue_system.infrastructure.vad.base_vad import BaseVad


# noinspection PyShadowingNames
class WebRtcVad(BaseVad):
    def __init__(self):
        super().__init__()
        self._vad = webrtcvad.Vad()
        # レベル2で検出する（0-3の整数値）
        self._vad.set_mode(3)
        self._threshold = 0.5

    def get_threshold(self) -> float:
        return self._threshold

    def detect(self, audio_chunk) -> float:
        # 320byte単位で分割して、1つでも音声と判定したら返する(16kHz, 16bit, 10ms)
        for i in range(0, len(audio_chunk), 320):
            slice_data = audio_chunk[i:i + 320]
            is_speech = self._vad.is_speech(slice_data, sample_rate=16000)
            if is_speech:
                return 1.0
        return 0.0


if __name__ == '__main__':

    pa = pyaudio.PyAudio()

    # マイクから入力するオーディオストリームを開く
    vad = WebRtcVad()
    audio = pyaudio.PyAudio()
    chunk_size = 1600

    while True:
        # set up audio recording
        # noinspection DuplicatedCode
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=chunk_size)

        loguru.logger.debug("音声検出待ち")
        while True:
            data = stream.read(chunk_size)
            result = vad.detect(data)
            loguru.logger.debug("result=" + str(result))
            if result >= vad.get_threshold():
                break
        loguru.logger.debug("")

        loguru.logger.debug("音声検出")
        reset_count = 0
        while True:
            data = stream.read(chunk_size)
            result = vad.detect(data)
            loguru.logger.debug("result=" + str(result))
            if result < vad.get_threshold():
                break
        loguru.logger.debug("")

        loguru.logger.debug("音声終了")

        stream.stop_stream()
        stream.close()
