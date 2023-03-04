# noinspection PyPackageRequirements


# noinspection PyMethodMayBeStatic
class BaseLanguageDetector:
    LANG_CODE_JP = "jp"
    LANG_CODE_EN = "en"

    def __init__(self):
        pass

    def detect(self, text: str) -> str:
        return ""
