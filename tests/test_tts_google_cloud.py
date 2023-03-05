from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS
from tests.test_utility import get_test_config


def test_tts():
    config = get_test_config()
    GoogleCloudTTS(config)
