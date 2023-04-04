from susumu_toolbox.infrastructure.obs.obs_client import OBSClient
from susumu_toolbox.infrastructure.config import Config


def test_obs():
    config = Config()
    OBSClient(config)
