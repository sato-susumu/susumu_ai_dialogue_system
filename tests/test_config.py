from omegaconf import OmegaConf

from susumu_toolbox.utility.config import Config


def test_default():
    config = Config()
    openai_api_key = config.get_openai_api_key()
    assert openai_api_key != ""


def test_set():
    config = Config()
    openai_api_key = config.get_openai_api_key()
    assert openai_api_key != ""

    config.set_openai_api_key("test")
    openai_api_key = config.get_openai_api_key()
    assert openai_api_key == "test"


def test_openai_api_key():
    config = Config()
    config._config = OmegaConf.create({"OpenAI": {"openai_api_key": "123"}})
    openai_api_key = config.get_openai_api_key()
    assert openai_api_key == "123"
