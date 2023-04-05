from susumu_ai_dialogue_system.infrastructure.obs.obs_client import OBSClient
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_obs():
    config = Config()
    OBSClient(config)
