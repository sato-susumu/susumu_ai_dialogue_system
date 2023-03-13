from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.utility.config import Config


def test_chat_connect_1():
    config = Config()
    chat = BaseChat(config)
    assert chat.is_init()

    chat.connect()
    assert chat.is_connected()

    chat.disconnect()
    assert chat.is_init()


def test_chat_connect_2():
    config = Config()
    chat = BaseChat(config)
    assert chat.is_init()

    # いきなり切断
    chat.disconnect()
    assert chat.is_init()

    chat.connect()
    assert chat.is_connected()

    # 接続中の接続
    chat.connect()
    assert chat.is_connected()
