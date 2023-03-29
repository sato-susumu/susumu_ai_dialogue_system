import speech_recognition as sr

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT, STTResult, STTEvent


class SRGoogleSyncSTT(BaseSTT):
    def __init__(self, config: Config):
        super().__init__(config)

        self._recognizer = sr.Recognizer()

    @BaseSTT.recognize_decorator
    def recognize(self):
        with sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source)
            self._event_publish(STTEvent.START)

            audio = self._recognizer.listen(source)

            try:
                text = self._recognizer.recognize_google(audio, language='ja-JP')
                self._event_publish(STTEvent.RESULT, STTResult(text, True))
            except sr.UnknownValueError:
                # 無音等でUnknownValueError例外が発生した場合は、空文字列を渡す
                self._event_publish(STTEvent.RESULT, STTResult("", True))
