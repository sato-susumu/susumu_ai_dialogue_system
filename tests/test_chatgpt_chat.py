import os

from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.utility.config import Config


def test_no_settings():
    config = Config()
    chat = ChatGPTChat(config)
    assert len(chat._messages) == 0


def test_settings():
    config = Config()
    settings_path = os.path.join(config.get_config_dir(), "system_settings.txt")
    chat = ChatGPTChat(config, settings_path)
    assert len(chat._messages) == 1


def test_prompt():
    config = Config()
    settings_path = os.path.join(config.get_config_dir(), "system_settings.txt")
    chat = ChatGPTChat(config, settings_path)
    assert len(chat._messages) == 1

    for i in range(10):
        chat._append_message("user", "test")
    prompt = chat._create_prompt()
    assert len(chat._messages) == 11
    assert len(prompt) == 11

    for i in range(10):
        chat._append_message("user", "test")
    prompt = chat._create_prompt()
    assert len(chat._messages) == 21
    assert len(prompt) == 20
