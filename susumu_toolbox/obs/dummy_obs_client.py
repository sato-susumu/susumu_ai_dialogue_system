from susumu_toolbox.obs.base_obs_client import BaseOBSClient
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,PyShadowingNames
class DummyOBSClient(BaseOBSClient):
    def __init__(self, config: Config):
        super().__init__(config)
