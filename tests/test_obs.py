from susumu_toolbox.obs.obs_client import OBSClient
from tests.test_utility import get_test_config


def test_obs():
    config = get_test_config()
    OBSClient(config)
