import threading
from enum import Enum

from event_channel.threaded_event_channel import ThreadedEventChannel

from susumu_toolbox.infrastructure.config import Config


class ChatResult:
    def __init__(self, text: str, quick_replies: list):
        self.text = text
        self.quick_replies = quick_replies


class ChatState(Enum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSING = 3


class BaseChat:
    lock = threading.Lock()

    # チャットモジュールが利用できる状態になったことを知らせるイベント
    EVENT_CHAT_OPEN = "chat_open"
    # チャットモジュールが利用できない状態になったことを知らせるイベント
    EVENT_CHAT_CLOSE = "chat_close"
    # チャットモジュールからのメッセージイベント
    EVENT_CHAT_MESSAGE = "chat_message"
    # チャットモジュールからのエラーイベント
    EVENT_CHAT_ERROR = "chat_error"

    def __init__(self, config: Config):
        self._config = config
        self.state: ChatState = ChatState.INIT
        self._event_channel = ThreadedEventChannel(blocking=False)

    def subscribe(self, event_name: str, func) -> None:
        self._event_channel.subscribe(event_name, func)

    def _set_state(self, new_state: ChatState) -> None:
        with self.lock:
            self.state = new_state

    def is_init(self) -> bool:
        return self.state == ChatState.INIT

    def is_connected(self) -> bool:
        return self.state == ChatState.CONNECTED

    def is_connecting(self) -> bool:
        return self.state == ChatState.CONNECTING

    def is_closing(self) -> bool:
        return self.state == ChatState.CLOSING

    def connect(self) -> None:
        if not self.is_init():
            return
        # BaseChatには接続先サーバーがないため、この時点で接続完了に関する処理を行う
        self._set_state(ChatState.CONNECTING)
        self._set_state(ChatState.CONNECTED)
        self._event_channel.publish(self.EVENT_CHAT_OPEN)
        # 接続先サーバーがある場合は、接続時にサーバーからメッセージを受け取り、そのメッセージを通知する
        # BaseChatには接続先サーバーがないため、空メッセージを通知する
        self._event_channel.publish(self.EVENT_CHAT_MESSAGE, ChatResult("", []))

    def disconnect(self) -> None:
        if not self.is_connected():
            return
        # BaseChatには接続先サーバーがないため、この時点で切断完了に関する処理を行う
        self._set_state(ChatState.CLOSING)
        self._set_state(ChatState.INIT)
        # BaseChatには接続先サーバーがないため、ダミーの通知を行う
        self._event_channel.publish(self.EVENT_CHAT_CLOSE, None, None)

    def send_message(self, text) -> None:
        pass
