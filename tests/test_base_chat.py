from susumu_toolbox.chat.base_chat import BaseChat
from tests.test_utility import get_test_config


def test_chat_connect_1():
    config = get_test_config()
    chat = BaseChat(config)
    assert chat.is_init()

    chat.connect()
    assert chat.is_connected()

    chat.disconnect()
    assert chat.is_init()


def test_chat_connect_2():
    config = get_test_config()
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
