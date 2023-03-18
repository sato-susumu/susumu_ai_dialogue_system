from susumu_toolbox.tts.google_cloud_tts import GoogleCloudTTS
from susumu_toolbox.tts.gtts_tts import GttsTTS
from susumu_toolbox.tts.pyttsx3_tts import Pyttsx3TTS
from susumu_toolbox.tts.voicevox_tts import VoicevoxTTS
from susumu_toolbox.utility.config import Config


class TTSTest:
    def __init__(self, config: Config):
        self._config = config

    def run(self, event) -> None:
        output_function = self._config.get_gui_output_function()
        if output_function == self._config.OUTPUT_FUNCTION_VOICEVOX:
            tts = VoicevoxTTS(self._config)
        elif output_function == self._config.OUTPUT_FUNCTION_GOOGLE_CLOUD:
            tts = GoogleCloudTTS(self._config)
        elif output_function == self._config.OUTPUT_FUNCTION_PYTTSX3:
            tts = Pyttsx3TTS(self._config)
        elif output_function == self._config.OUTPUT_FUNCTION_GTTS:
            tts = GttsTTS(self._config)
        else:
            raise ValueError(f"Invalid output_function: {output_function}")

        tts.tts_play_async("テストです。")


if __name__ == "__main__":
    _config = Config()
    _config.load()
    TTSTest(_config).run()
