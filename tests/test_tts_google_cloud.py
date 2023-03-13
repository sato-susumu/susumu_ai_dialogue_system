from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS
from susumu_toolbox.utility.config import Config


def test_tts():
    config = Config()
    GoogleCloudTTS(config)
