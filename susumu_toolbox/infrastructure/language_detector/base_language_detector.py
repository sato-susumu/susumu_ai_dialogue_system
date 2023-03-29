import logging


# noinspection PyMethodMayBeStatic
class BaseLanguageDetector:
    # 定数名はISO 639-1。中身は暫定でlinguaに合わせる
    LANG_CODE_JA = "jp"
    LANG_CODE_EN = "en"

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def detect(self, text: str) -> str:
        return ""
