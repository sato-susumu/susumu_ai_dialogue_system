from samples.gui.gui_events import GuiEvents
from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS
from susumu_toolbox.tts.gtts_tts import GttsTTS
from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.utility.config import Config


class TTSTest:
    def __init__(self, config: Config):
        self._config = config

    def run(self, event) -> None:
        if event == GuiEvents.VOICEVOX_TEST:
            tts = VoicevoxTTS(self._config)
        elif event == GuiEvents.GOOGLE_CLOUD_TTS_TEST:
            tts = GoogleCloudTTS(self._config)
        elif event == GuiEvents.PYTTSX3_TEST:
            tts = Pyttsx3TTS(self._config)
        else:
            tts = GttsTTS(self._config)
        tts.tts_play_async("テストです。")
