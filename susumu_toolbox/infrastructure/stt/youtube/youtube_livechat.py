import datetime
import re

import dateutil.parser
import requests

from susumu_toolbox.infrastructure.config import Config


# noinspection PyMethodMayBeStatic, PyShadowingNames
class YouTubeLiveChatMessage:
    _custom_emoji_pattern = re.compile(r":[a-zA-Z0-9_]+:")

    def __init__(self, item):
        # displayMessageはスパチャの場合は、'¥価格 from 名前: "メッセージ"'という形式になっている。
        # item["snippet"]["type"]によってもっと処理を分けるべき？

        self.original_message = item["snippet"]["displayMessage"]
        self.name = item["authorDetails"]["displayName"]
        self.datetime_utc = self.parse_utc_datetime_str(item["snippet"]["publishedAt"])
        self.message = self._delete_custom_emoji(self.original_message)

    def parse_utc_datetime_str(self, datetime_str: str) -> datetime.datetime:
        return dateutil.parser.parse(datetime_str)

    def _delete_custom_emoji(self, text: str) -> str:
        return self._custom_emoji_pattern.sub("", text)


# noinspection PyMethodMayBeStatic
class YouTubeLiveChat:
    # もっと設計をしっかりするなら youtube_livechat_messages や pytchatを参考にする？
    def __init__(self, config: Config):
        self._next_page_token = None
        self._api_key = config.get_gcp_youtube_data_api_key()
        self._youtube_url = config.get_youtube_live_url()
        self._chat_id = None
        self._video_id = None

    def _get_video_id(self):
        if "https://www.youtube.com/watch?v=" not in self._youtube_url:
            raise ValueError("YouTubeのURLが不正です。")
        video_id = self._youtube_url.replace('https://www.youtube.com/watch?v=', '')
        return video_id

    def _get_chat_id(self):
        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': self._api_key,
            'id': self._video_id,
            'part': 'liveStreamingDetails'
        }
        response = requests.get(url, params=params)
        if response.status_code // 100 != 2:
            raise ValueError(f"{response.status_code}: {response.text}")
        data = response.json()

        details = data['items'][0]['liveStreamingDetails']
        if 'activeLiveChatId' in details.keys():
            return details['activeLiveChatId']
        return None

    def fetch_messages(self):
        if self._video_id is None:
            self._video_id = self._get_video_id()
        if self._chat_id is None:
            self._chat_id = self._get_chat_id()
            if self._chat_id is None:
                raise ValueError("YouTubeライブチャットIDの取得に失敗しました。YouTubeのライブチャットが開始されいないか、ライブチャットが無効になっています。")

        params = {
            'key': self._api_key,
            'liveChatId': self._chat_id,
            'part': 'id, snippet, authorDetails'
        }
        if self._next_page_token:
            params['pageToken'] = self._next_page_token

        # API仕様は https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list 参照
        # itemsの仕様は https://developers.google.com/youtube/v3/live/docs/liveChatMessages 参照
        url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
        response = requests.get(url, params=params)
        if response.status_code // 100 != 2:
            raise ValueError(f"{response.status_code}: {response.text}")
        result = response.json()

        messages = []
        if "items" not in result.keys():
            return messages
        for item in result['items']:
            messages.append(YouTubeLiveChatMessage(item))

        self._next_page_token = result['nextPageToken']
        return messages
