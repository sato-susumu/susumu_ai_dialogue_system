import os

from susumu_toolbox.utility.config import Config


def get_test_config() -> Config:
    config = Config()
    file_path = os.path.join(config.get_config_dir(), "sample_config.yaml")
    config.load_config(file_path)
    return config
