import datetime
import logging
import time

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.limited_fifo import LimitedFIFO
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT, STTResult, STTEvent
from susumu_toolbox.infrastructure.stt.youtube.message_filter import MessageFilter
from susumu_toolbox.infrastructure.stt.youtube.youtube_livechat import YouTubeLiveChat


class YoutubePseudSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)

        self._timezone_jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        self._client = YouTubeLiveChat(config)
        self._message_filter = MessageFilter()
        self._fifo = LimitedFIFO(5)

    def _fetch_message(self):
        message_list = self._client.fetch_messages()

        message_list = self._message_filter.exclude_empty_message(message_list)
        if len(message_list) >= 3:
            message_list = self._message_filter.choose_random_items(message_list, num_items=3)

        # for message in message_list:
        #     datetime_jst = message.datetime_utc.astimezone(self._timezone_jst)
        #     datetime_str = datetime_jst.strftime('%H:%M:%S.%f')[:-3]
        #     self._logger.debug(f"{datetime_str}: name={message.name} message={message.message}")

        for message in message_list:
            self._fifo.put(message)

    @BaseSTT.recognize_decorator
    def recognize(self):
        self._event_publish(STTEvent.START)
        self._fetch_message()
        if self._fifo.is_empty():
            self._event_publish(STTEvent.RESULT, STTResult("", True))
        else:
            message = self._fifo.get()
            # self._logger.debug(f"message={message.message}")
            self._event_publish(STTEvent.RESULT, STTResult(message.message, True))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    _config = Config()
    _config.search_and_load()
    while True:
        YoutubePseudSTT(_config).recognize()
        time.sleep(5)
