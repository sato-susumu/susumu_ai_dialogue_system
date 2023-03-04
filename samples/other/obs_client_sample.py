import logging
import time

from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.utility.config_manager import ConfigManager

logging.basicConfig(level=logging.DEBUG)

config = ConfigManager()
config.load_config()

host = config.get_obs_host()
port = config.get_obs_port_no()
password = config.get_obs_password()

client = OBSClient()
client.connect(host, port, password)
for i in range(30):
    client.set_text("scene1", "text1", f"テキスト1の内容 No.{i}")
    client.set_text("scene1", "text2", f"テキスト2の内容 No.{i}")
    time.sleep(1)
client.disconnect()
