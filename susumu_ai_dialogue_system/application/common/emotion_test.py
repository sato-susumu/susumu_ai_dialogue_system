from loguru import logger

from susumu_ai_dialogue_system.application.common.function_factory import FunctionFactory
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.wrime_emotion_client import WrimeEmotionClient
from susumu_ai_dialogue_system.infrastructure.tts.base_tts import TTSEvent


# noinspection PyMethodMayBeStatic
class EmotionTest:
    def __init__(self, config: Config):
        self._config = config
        self._emotion_mode = WrimeEmotionClient(config)

    def run(self, text) -> None:
        max_emotion, max_emotion_value, emotion_dic = self._emotion_mode.get_max_emotion(text)
        output_emotions = ""
        for key, value in emotion_dic.items():
            output_emotions += f"  {key.value}={value:0.2f}"
        logger.info(f"text: {text}")
        logger.info(f"max_emotion: {max_emotion}, max_emotion_value: {max_emotion_value}")
        logger.info(f"emotions: {output_emotions}")

        raw_dic = self._emotion_mode.get_raw_emotion(text)
        output_raw_emotions = ""
        for key, value in raw_dic.items():
            output_raw_emotions += f"  {key}={value:0.2f}"
        logger.info(f"raw_emotions: {output_raw_emotions}")


if __name__ == "__main__":
    _config = Config()
    _config.search_and_load()
    EmotionTest(_config).run("テスト")

