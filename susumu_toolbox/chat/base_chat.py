from multiprocessing import Value

from event_channel.threaded_event_channel import ThreadedEventChannel


class ChatResult:
    def __init__(self, text: str, quick_replies: list):
        self.text = text
        self.quick_replies = quick_replies


class BaseChat:
    _STATE_INIT = 0
    _STATE_CONNECTING = 1
    _STATE_CONNECTED = 2
    _STATE_CLOSING = 3

    # チャットモジュールが利用できる状態になったことを知らせるイベント
    EVENT_CHAT_OPEN = "chat_open"
    # チャットモジュールが利用できない状態になったことを知らせるイベント
    EVENT_CHAT_CLOSE = "chat_close"
    # チャットモジュールからのメッセージイベント
    EVENT_CHAT_MESSAGE = "chat_message"
    # チャットモジュールからのエラーイベント
    EVENT_CHAT_ERROR = "chat_error"

    def __init__(self):
        self.state = Value('i', self._STATE_INIT)
        self._event_channel = ThreadedEventChannel(blocking=False)

    def subscribe(self, event_name: str, func) -> None:
        self._event_channel.subscribe(event_name, func)

    def _set_state(self, new_state: int) -> None:
        with self.state.get_lock():
            self.state.value = new_state

    def is_init(self) -> bool:
        return self.state.value == self._STATE_INIT

    def is_connected(self) -> bool:
        return self.state.value == self._STATE_CONNECTED

    def is_connecting(self) -> bool:
        return self.state.value == self._STATE_CONNECTING

    def is_closing(self) -> bool:
        return self.state.value == self._STATE_CLOSING

    def connect(self, host: str = None, port_no: int = None) -> None:
        if not self.is_init():
            return
        self._set_state(self._STATE_CONNECTING)
        self._set_state(self._STATE_CONNECTED)

    def disconnect(self) -> None:
        if not self.is_connected():
            return
        self._set_state(self._STATE_CLOSING)
        self._set_state(self._STATE_INIT)

    def send_message(self, text) -> None:
        pass
