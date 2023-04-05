from susumu_ai_dialogue_system.infrastructure.chat.chatgpt_chat import ChatGPTChat
from susumu_ai_dialogue_system.infrastructure.config import Config


def test_settings():
    config = Config()
    chat = ChatGPTChat(config)
    assert len(chat._messages) == 1


def test_prompt():
    config = Config()
    chat = ChatGPTChat(config)
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
