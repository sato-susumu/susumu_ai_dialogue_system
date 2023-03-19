from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.system_setting import SystemSettings


def test_settings():
    config = Config()
    system_settings = SystemSettings(config)
    chat = ChatGPTChat(config, system_settings)
    assert len(chat._messages) == 1


def test_prompt():
    config = Config()
    system_settings = SystemSettings(config)
    chat = ChatGPTChat(config, system_settings)
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
