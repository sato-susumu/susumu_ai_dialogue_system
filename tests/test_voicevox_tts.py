from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS


def test_tts_play():
    tts = VoicevoxTTS()
    tts.tts_play('音声合成結果を再生しています')
    tts.tts_play('音声合成結果を再生しています2')


def test_tts_save_mp3():
    tts = VoicevoxTTS()
    tts.tts_save_mp3('音声合成結果をmp3ファイルとして出力しました', 'voicevox_tts.mp3')


def test_tts_save_wav():
    tts = VoicevoxTTS()
    tts.tts_save_wav('音声合成結果をwavファイルとして出力しました', 'voicevox_tts.wav')
