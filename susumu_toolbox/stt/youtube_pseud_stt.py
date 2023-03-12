import datetime
import time

from susumu_toolbox.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.stt.youtube.message_filter import MessageFilter
from susumu_toolbox.stt.youtube.youtube_livechat import YouTubeLiveChat
from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.limited_fifo import LimitedFIFO


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
        #     print(f"{datetime_str}: name={message.name} message={message.message}")

        for message in message_list:
            self._fifo.put(message)

    def recognize(self, audio_stream=None):
        self._event_channel.publish(self.EVENT_STT_START)

        self._fetch_message()
        if self._fifo.is_empty():
            self._event_channel.publish(self.EVENT_STT_RESULT, STTResult("", True))
        else:
            message = self._fifo.get()
            # print(f"message={message.message}")
            self._event_channel.publish(self.EVENT_STT_RESULT, STTResult(message.message, True))

        self._event_channel.publish(self.EVENT_STT_END)


if __name__ == '__main__':
    _config = Config()
    _config.load_config()
    while True:
        YoutubePseudSTT(_config).recognize()
        time.sleep(5)
