from susumu_toolbox.tts.gtts_tts import GttsTTS


def test_tts_play():
    tts = GttsTTS()
    tts.tts_play('音声合成結果を再生しています')
    tts.tts_play('音声合成結果を再生しています2')


def test_tts_save_mp3():
    tts = GttsTTS()
    tts.tts_save_mp3('音声合成結果をmp3ファイルとして出力しました', 'gtts.mp3')


def test_tts_save_wav():
    tts = GttsTTS()
    tts.tts_save_wav('音声合成結果をwavファイルとして出力しました', 'gtts.wav')
