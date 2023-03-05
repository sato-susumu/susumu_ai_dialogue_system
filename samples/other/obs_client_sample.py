import logging
import time

from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.utility.config import Config

logging.basicConfig(level=logging.DEBUG)

config = Config()
config.load_config()
client = OBSClient(config)
client.connect()
for i in range(30):
    client.set_text("scene1", "text1", f"テキスト1の内容 No.{i}")
    client.set_text("scene1", "text2", f"テキスト2の内容 No.{i}")
    time.sleep(1)
client.disconnect()
