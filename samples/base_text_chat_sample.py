import time
import traceback

from six.moves import queue

from susumu_toolbox.chat.base_chat import BaseChat, ChatResult
from susumu_toolbox.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,DuplicatedCode
class BaseTextChatSample:
    def __init__(self, config: Config):
        self._config = config
        self._chat_message_queue = queue.Queue()
        self._stt_message_queue = queue.Queue()
        self._translator = self.create_translator()
        self._chat = self.create_chat()
        self._chat.subscribe(self._chat.EVENT_CHAT_OPEN, self._on_chat_open)
        self._chat.subscribe(self._chat.EVENT_CHAT_CLOSE, self._on_chat_close)
        self._chat.subscribe(self._chat.EVENT_CHAT_MESSAGE, self._on_chat_message)
        self._chat.subscribe(self._chat.EVENT_CHAT_ERROR, self._on_chat_error)

        speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]

        self._stt = self.create_stt(speech_contexts=speech_contexts)
        self._stt.subscribe(self._stt.EVENT_STT_START, self._on_stt_start)
        self._stt.subscribe(self._stt.EVENT_STT_END, self._on_stt_end)
        self._stt.subscribe(self._stt.EVENT_STT_RESULT, self._on_stt_result)
        self._stt.subscribe(self._stt.EVENT_STT_DEBUG_MESSAGE, self._on_stt_debug_message)
        self._stt.subscribe(self._stt.EVENT_STT_ERROR, self._on_stt_error)

    def create_chat(self) -> BaseChat:
        return BaseChat(self._config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return BaseSTT(self._config)

    def create_translator(self) -> BaseTranslator:
        return BaseTranslator(self._config)

    def _on_chat_open(self):
        print("_on_chat_open")

    def _on_chat_close(self, status_code, close_msg):
        print(f"_on_chat_close status_code={status_code} close_msg={close_msg}")
        self._chat_message_queue.put(None)

    def _on_chat_message(self, message: ChatResult):
        print("_on_chat_message")
        self._chat_message_queue.put(message)

    def _on_chat_error(self, error: Exception):
        print(f"_on_chat_error exception={error}")

    def _on_stt_start(self):
        # print("stt start")
        pass

    def _on_stt_end(self):
        # print("stt end")
        pass

    def _on_stt_result(self, result: STTResult):
        if result.is_timed_out:
            print('stt final(timeout):' + result.text)
        elif result.is_final:
            print('stt final:' + result.text)
            self._stt_message_queue.put(result)
        else:
            print('stt not final:' + result.text)

    def _on_stt_debug_message(self, x):
        # # デバッグ出力
        # print("------------------")
        # print(x)
        pass

    def _on_stt_error(self, e):
        print(e)

    def _wait_input(self) -> str:
        while True:
            print("ME(発言を入力してリターンを押してください。終了する場合はbyeと入力): ", end="")

            self._stt.recognize()
            print("STTメッセージキュー待機")
            stt_message = self._stt_message_queue.get(block=True, timeout=None)
            print("STTメッセージキュー取得")
            if stt_message is None:
                return "bye"
            input_text = stt_message.text
            if input_text == "":
                print("入力 失敗")
                continue
            return input_text

    def run_once(self) -> None:
        # noinspection PyBroadException
        try:
            self._chat.connect()

            while self._chat.is_connecting():
                time.sleep(1)

            while self._chat.is_connected():
                print("CHATメッセージキュー待機")
                chat_message = self._chat_message_queue.get(block=True, timeout=None)
                print("CHATメッセージキュー取得")
                if chat_message is None:
                    break
                message_text = chat_message.text
                message_text = self._translator.translate(message_text, self._translator.LANG_CODE_JA_JP)
                print("Bot: " + message_text)
                quick_replies = chat_message.quick_replies
                if quick_replies is not None and len(quick_replies) > 0:
                    print(f"\nOptions: [{'|'.join(quick_replies)}]")

                input_text = self._wait_input()

                if input_text == "bye":
                    self._chat.disconnect()
                else:
                    text = self._translator.translate(input_text, self._translator.LANG_CODE_EN_US)
                    print("Bot 返事待ち開始")
                    self._chat.send_message(text)
                    print("Bot 返事待ち完了 ")
        except Exception as e:
            print(traceback.format_exc())  # いつものTracebackが表示される
            print("エラーが発生しましたが処理を継続します！")
        finally:
            self._chat.disconnect()

    def run_forever(self) -> None:
        print("run_forever")
        while True:
            self.run_once()
