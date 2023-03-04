import json
import threading
import time
import uuid
from typing import Optional

import websocket

from susumu_toolbox.chat.base_chat import BaseChat, ChatResult


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class ParlAIChat(BaseChat):

    def __init__(self):
        super().__init__()
        self.ws_app = None
        self.uuid = self._get_uuid()

    def _get_uuid(self) -> str:
        return str(uuid.uuid4())

    def _on_message(self, ws_app, message) -> None:
        if self.is_closing():
            return
        incoming_message = json.loads(message)
        text = incoming_message['text']
        # noinspection SpellCheckingInspection
        if text == 'Welcome to the overworld for the ParlAI messenger chatbot demo. ' \
                   'Please type "begin" to start, or "exit" to exit':
            self._send_message("begin")
            return
        # if text == 'Welcome to the ParlAI Chatbot demo. You are now paired with a bot -' \
        #            ' feel free to send a message.Type [DONE] to finish the chat,' \
        #            ' or [RESET] to reset the dialogue history.':
        #     incoming_message['text'] = "hello"
        chat_result = ChatResult(text, incoming_message.get('quick_replies'))
        self._event_channel.publish(self.EVENT_CHAT_MESSAGE, chat_result)

    def _on_error(self, ws_app, error: Exception) -> None:
        self._event_channel.publish(self.EVENT_CHAT_ERROR, error)

    def _on_open(self, ws_app) -> None:
        self._set_state(self._STATE_CONNECTED)
        # オープン時に適当に送信
        self._send_message("")
        self._event_channel.publish(self.EVENT_CHAT_OPEN)

    def _on_close(self, ws_app, status_code: Optional[int], close_msg: Optional[str]) -> None:
        self._set_state(self._STATE_INIT)
        self._event_channel.publish(self.EVENT_CHAT_CLOSE, status_code, close_msg)

    def _send_message(self, text: str) -> None:
        data = {'id': self.uuid, 'text': text}
        json_data = json.dumps(data)
        self.ws_app.send(json_data)

    def connect(self, host: str = "127.0.0.1", port_no: int = 35496) -> None:
        if not self.is_init():
            return
        self._set_state(self._STATE_CONNECTING)

        self.ws_app = websocket.WebSocketApp(
            f"ws://{host}:{port_no}/websocket",
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

        def _run_forever() -> None:
            self.ws_app.run_forever()

        threading.Thread(target=_run_forever).start()

    def disconnect(self) -> None:
        if not self.is_connected():
            return
        self._set_state(self._STATE_CLOSING)
        # 終了時には[DONE] と EXITの両方を送る必要があるらしい。
        self._send_message("[DONE]")
        # 元のサンプルでも2秒待っていたので、2秒待つ
        time.sleep(2)
        self._send_message("exit")
        self.ws_app.close()
        self._set_state(self._STATE_INIT)

    def send_message(self, text) -> None:
        if not self.is_connected():
            return
        self._send_message(text)
