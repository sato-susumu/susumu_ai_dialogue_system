import pyaudio
from event_channel.threaded_event_channel import ThreadedEventChannel
from six.moves import queue


class STTResult:
    def __init__(self, text: str, is_final: bool, is_timed_out: bool = False):
        self.text = text
        self.is_final = is_final
        self.is_timed_out = is_timed_out


class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # スレッドセーフのオーディオ格納バッファ。サイズ無制限
        self._buff = queue.Queue()
        self._audio_interface = None
        self._audio_stream = None
        self.closed = True

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # コールバック
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def _stop_generator(self):
        self._buff.put(None)

    def close(self):
        if not self.closed:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
            self.closed = True
            self._stop_generator()
            self._audio_interface.terminate()

    # noinspection PyUnusedLocal
    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        # コールバックが呼ばれたときにバッファにデータを格納
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """ジェネレーターメソッド"""
        while not self.closed:
            # キューからの取り出し
            # データが終わったときにはNoneが積まれているので、Noneだった場合は戻る
            chunk = self._buff.get(block=True, timeout=None)
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    # データがあれば、さらに取得。
                    # block=Falseなので、データがなければqueue.Empty例外発生
                    chunk = self._buff.get(block=False)
                except queue.Empty:
                    # バッファが空になったらbreak
                    break
                # データが終わったときにはNoneが積まれているので、Noneだった場合は戻る
                if chunk is None:
                    return
                data.append(chunk)

            yield b"".join(data)


class BaseSTT:
    EVENT_STT_START = "stt_start"
    EVENT_STT_END = "stt_end"
    EVENT_STT_RESULT = "stt_result"
    EVENT_STT_DEBUG_MESSAGE = "stt_debug_message"
    EVENT_STT_ERROR = "stt_error"

    def __init__(self):
        self._event_channel = ThreadedEventChannel(blocking=False)

    def subscribe(self, event_name: str, func):
        self._event_channel.subscribe(event_name, func)

    def recognize(self):
        pass
