from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS


def test_tts_play():
    tts = GoogleCloudTTS()
    tts.tts_play('音声合成結果を再生しています')
    tts.tts_play('音声合成結果を再生しています2')


def test_tts_save_mp3():
    tts = GoogleCloudTTS()
    tts.tts_save_mp3('音声合成結果をmp3ファイルとして出力しました', 'google_cloud_tts.mp3')


def test_tts_save_wav():
    tts = GoogleCloudTTS()
    tts.tts_save_wav('音声合成結果をwavファイルとして出力しました', 'google_cloud_tts.wav')
