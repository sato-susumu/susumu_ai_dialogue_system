from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.obs.base_obs_client import BaseOBSClient


# noinspection PyMethodMayBeStatic,PyShadowingNames
class DummyOBSClient(BaseOBSClient):
    def __init__(self, config: Config):
        super().__init__(config)
