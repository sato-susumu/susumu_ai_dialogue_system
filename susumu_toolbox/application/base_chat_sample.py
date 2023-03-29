import logging
import queue
from threading import Event
from typing import Optional

from susumu_toolbox.application.common.function_factory import FunctionFactory
from susumu_toolbox.application.common.stt_helper import STTHelper
from susumu_toolbox.infrastructure.chat.base_chat import BaseChat, ChatResult, ChatEvent
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.infrastructure.stt.sr_google_sync_stt import SRGoogleSyncSTT
from susumu_toolbox.infrastructure.system_setting import SystemSettings
from susumu_toolbox.infrastructure.translation.base_translator import BaseTranslator
from susumu_toolbox.infrastructure.translation.dummy_translator import DummyTranslator
from susumu_toolbox.infrastructure.tts.base_tts import BaseTTS, TTSEvent


# noinspection PyMethodMayBeStatic,DuplicatedCode
class BaseChatSample:
    def __init__(self, config: Config, system_settings: SystemSettings):
        self._logger = logging.getLogger(__name__)
        self._config = config
        self._system_settings = system_settings
        self._chat_message_queue = queue.Queue()
        self._stt_message_queue = queue.Queue()
        self._exit_requested_event = Event()

        # speech_contexts = ["後退", "前進", "右旋回", "左旋回", "バック"]
        speech_contexts = []
        self._stt = self.create_stt(speech_contexts=speech_contexts)
        self._stt_helper = STTHelper(config)
        self._translator = self.create_translator()
        self._chat = self.create_chat()
        self._tts = self.create_tts()
        self._obs = self.create_obs_client()
        self._emotion_model = self.create_emotion_model()
        self._app_controller = self.create_app_controller()

        self._chat.event_subscribe(ChatEvent.OPEN, self._on_chat_open)
        self._chat.event_subscribe(ChatEvent.CLOSE, self._on_chat_close)
        self._chat.event_subscribe(ChatEvent.MESSAGE, self._on_chat_message)
        self._chat.event_subscribe(ChatEvent.ERROR, self._on_chat_error)

        self._tts.event_subscribe(TTSEvent.START, self._on_tts_start)
        self._tts.event_subscribe(TTSEvent.END, self._on_tts_end)

    def create_chat(self) -> BaseChat:
        chat = FunctionFactory.create_chat(self._config, self._system_settings)
        self._logger.debug(f"chat:{chat}")
        return chat

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        stt = FunctionFactory.create_stt(self._config, speech_contexts)
        self._logger.debug(f"stt:{stt}")
        return stt

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)

    def create_tts(self) -> BaseTTS:
        tts = FunctionFactory.create_tts(self._config)
        self._logger.debug(f"tts:{tts}")
        return tts

    def create_obs_client(self):
        obs = FunctionFactory.create_obs_client(self._config)
        self._logger.debug(f"obs:{obs}")
        return obs

    def create_emotion_model(self):
        emotion_model = FunctionFactory.create_emotion_model(self._config)
        self._logger.debug(f"emotion model:{emotion_model}")
        return emotion_model

    def create_app_controller(self):
        controller = FunctionFactory.create_app_controller(self._config)
        self._logger.debug(f"app controller:{controller}")
        return controller

    def _on_tts_start(self):
        self._logger.debug("_on_tts_start")

    def _on_tts_end(self):
        self._logger.debug("_on_tts_end")
        self._app_controller.set_emotion(Emotion.NEUTRAL)

    def _on_chat_open(self):
        self._logger.debug("_on_chat_open")

    def _on_chat_close(self, status_code, close_msg):
        self._logger.debug(f"_on_chat_close status_code={status_code} close_msg={close_msg}")
        self._chat_message_queue.put(None)

    def _on_chat_message(self, message: ChatResult):
        self._logger.debug("_on_chat_message")
        self._chat_message_queue.put(message)

    def _on_chat_error(self, error: Exception):
        self._logger.debug(f"_on_chat_error exception={error}")

    def _on_stt_start(self):
        console_message = self._stt_helper.get_start_message_for_console()
        if console_message is not None:
            self._logger.debug(console_message)
        caption_message = self._stt_helper.get_start_message_for_caption()
        if caption_message is not None:
            self._obs.set_user_utterance_text(caption_message)

    def _on_stt_result(self, result: STTResult):
        if result.is_final:
            if result.is_timed_out:
                self._logger.debug('stt final(timeout):' + result.text)
            else:
                self._logger.debug('stt final:' + result.text)
            self._stt_message_queue.put(result)
        else:
            self._logger.debug('stt not final:' + result.text)

    def _on_stt_end(self):
        # self._logger.debug("stt end")
        pass

    def _on_stt_debug_message(self, x):
        # # デバッグ出力
        # self._logger.debug("------------------")
        # self._logger.debug(x)
        pass

    def _on_stt_error(self, e):
        self._logger.debug(e)

    def _connect_all(self):
        self._obs.connect()
        self._obs.set_user_utterance_text("")
        self._obs.set_ai_utterance_text("")
        self._app_controller.connect()
        self._chat.connect()

    def _disconnect_all(self):
        self._obs.set_user_utterance_text("")
        self._obs.set_ai_utterance_text("")
        self._obs.disconnect()
        self._app_controller.disconnect()
        self._chat.disconnect()

    def _wait_user_input(self) -> str:
        while True:
            if type(self._stt) == SRGoogleSyncSTT:
                self._logger.debug("音声認識 準備中")
            self._stt.recognize()
            self._logger.debug("STTメッセージキュー待機")
            stt_message = self._stt_message_queue.get(block=True, timeout=None)
            self._logger.debug("STTメッセージキュー取得")
            if stt_message is None:
                return "bye"
            input_text = stt_message.text
            if input_text == "終了":
                return "bye"
            if input_text == "":
                continue
            return input_text

    def _present_ai_message(self, text: str, obs_ai_utterance_text: Optional[str], tts_async_playback: bool = True):
        self._logger.debug("Present AI message. AI: " + text)
        text = self._translator.translate(text, self._translator.LANG_CODE_JA_JP)

        self._present_ai_emotion(text)

        if obs_ai_utterance_text:
            self._obs.set_ai_utterance_text(text)

        if tts_async_playback:
            self._tts.tts_play_async(text)
        else:
            self._tts.tts_play_sync(text)

    def _present_ai_emotion(self, ai_text: str):
        max_emotion, max_emotion_value, raw_dict = self._emotion_model.get_max_emotion(ai_text)
        self._logger.debug(f"max_emotion: {max_emotion}, max_emotion_value: {max_emotion_value}")
        self._logger.debug(f"raw_result:{raw_dict}")
        if max_emotion_value > 0.4:
            self._app_controller.set_emotion(max_emotion)
        else:
            self._app_controller.set_emotion(Emotion.NEUTRAL)

    def _present_quick_replies(self, quick_replies: list):
        if quick_replies is not None and len(quick_replies) > 0:
            self._logger.debug(f"\nOptions: [{'|'.join(quick_replies)}]")

    def _request_ai_message(self, *, user_text: str, obs_ai_utterance_text: Optional[str]):
        self._logger.debug("Request AI message.")

        if obs_ai_utterance_text:
            self._obs.set_ai_utterance_text(obs_ai_utterance_text)

        text = self._translator.translate(user_text, self._translator.LANG_CODE_EN_US)
        self._logger.debug("AI 返事待ち開始")
        self._chat.send_message(text)
        self._logger.debug("AI 返事待ち完了 ")

    def _wait_ai_response(self) -> ChatResult:
        self._logger.debug("CHATメッセージキュー待機")
        ai_result = self._chat_message_queue.get(block=True, timeout=None)
        self._logger.debug("CHATメッセージキュー取得")
        return ai_result

    def run_forever(self) -> None:
        self._logger.debug("run_forever")
        while self._exit_requested_event.is_set() is False:
            self.run_once()

    def run_once(self) -> None:
        self._logger.debug("run_once")
