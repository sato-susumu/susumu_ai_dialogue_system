from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.obs.base_obs_client import BaseOBSClient


# noinspection PyMethodMayBeStatic,PyShadowingNames
class DummyOBSClient(BaseOBSClient):
    def __init__(self, config: Config):
        super().__init__(config)
