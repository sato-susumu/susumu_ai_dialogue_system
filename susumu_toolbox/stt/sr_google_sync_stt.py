import speech_recognition as sr

from susumu_toolbox.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.utility.config import Config


class SRGoogleSyncSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)
        self._recognizer = sr.Recognizer()

    def recognize(self, audio_stream=None):
        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source)
            self._event_channel.publish(self.EVENT_STT_START)

            audio = self._recognizer.listen(source)

            try:
                text = self._recognizer.recognize_google(audio, language='ja-JP')
                self._event_channel.publish(self.EVENT_STT_RESULT, STTResult(text, True))
            except sr.UnknownValueError:
                # 無音等でUnknownValueError例外が発生した場合は、空文字列を渡す
                self._event_channel.publish(self.EVENT_STT_RESULT, STTResult("", True))
            except Exception as e:
                self._event_channel.publish(self.EVENT_STT_ERROR, e)

        self._event_channel.publish(self.EVENT_STT_END)
