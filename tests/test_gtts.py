from susumu_toolbox.tts.gtts_tts import GttsTTS
from susumu_toolbox.utility.config import Config


def test_tts_play():
    config = Config()
    config.load_config()

    tts = GttsTTS(config)
    tts.tts_play('音声合成結果を再生しています')
    tts.tts_play('音声合成結果を再生しています2')


def test_tts_save_mp3():
    config = Config()
    config.load_config()

    tts = GttsTTS(config)
    tts.tts_save_mp3('音声合成結果をmp3ファイルとして出力しました', 'gtts.mp3')


def test_tts_save_wav():
    config = Config()
    config.load_config()

    tts = GttsTTS(config)
    tts.tts_save_wav('音声合成結果をwavファイルとして出力しました', 'gtts.wav')
