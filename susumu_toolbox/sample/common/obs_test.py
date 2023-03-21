import logging
import time

from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.utility.config import Config


class OBSTest:
    def __init__(self, config: Config):
        self._config = config

    def run(self):
        client = OBSClient(self._config)
        client.connect()
        for i in range(10):
            client.set_user_utterance_text(f"テキスト1の内容 No.{i}")
            client.set_ai_utterance_text(f"テキスト2の内容 No.{i}")
            time.sleep(1)
        client.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    _config = Config()
    _config.search_and_load()
    OBSTest(_config).run()
