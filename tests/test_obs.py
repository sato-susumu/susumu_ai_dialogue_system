from susumu_toolbox.obs.obs_client import OBSClient
from susumu_toolbox.utility.config import Config


def test_obs():
    config = Config()
    OBSClient(config)
