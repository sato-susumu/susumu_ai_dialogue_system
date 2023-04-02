from enum import Enum
from queue import Queue, Empty

import pyaudio
from event_channel.threaded_event_channel import ThreadedEventChannel

from susumu_toolbox.infrastructure.config import Config


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
        self._buff = Queue()
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
                except Empty:
                    # バッファが空になったらbreak
                    break
                # データが終わったときにはNoneが積まれているので、Noneだった場合は戻る
                if chunk is None:
                    return
                data.append(chunk)

            yield b"".join(data)


class STTEvent(Enum):
    # 音声認識(単発)の開始イベント
    START = "stt_start"
    # 音声認識(単発)の終了イベント
    END = "stt_end"
    # 音声認識(単発)の結果を知らせるイベント
    #   次のケースがある
    #     音声認識の途中経過
    #     音声認識の最終結果
    #     タイムアウトによる音声認識の最終結果
    RESULT = "stt_result"
    # 音声認識(単発)のデバッグメッセージイベント
    DEBUG_MESSAGE = "stt_debug_message"
    # 音声認識(単発)のエラーイベント
    ERROR = "stt_error"


# noinspection PyMethodMayBeStatic
class BaseSTT:
    def __init__(self, config: Config):
        self._config = config

        self.__event_channel = ThreadedEventChannel(blocking=False)

    def event_subscribe(self, event_name: STTEvent, func):
        self.__event_channel.subscribe(event_name.value, func)

    def _event_publish(self, event: STTEvent, *args, **kwargs):
        self.__event_channel.publish(event.value, *args, **kwargs)

    def update_config(self, config: Config):
        self._config = config

    def recognize(self):
        pass

    @staticmethod
    def recognize_decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                self._event_publish(STTEvent.RESULT, STTResult("", True))
                self._event_publish(STTEvent.ERROR, e)
                raise
            finally:
                self._event_publish(STTEvent.END)

            return result

        return wrapper
