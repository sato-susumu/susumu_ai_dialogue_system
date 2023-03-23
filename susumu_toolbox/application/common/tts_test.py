from susumu_toolbox.application.common.function_factory import FunctionFactory
from susumu_toolbox.infrastructure.config import Config


class TTSTest:
    def __init__(self, config: Config):
        self._config = config

    def run(self) -> None:
        tts = FunctionFactory.create_tts(self._config)
        tts.tts_play_async("テストです。")


if __name__ == "__main__":
    _config = Config()
    _config.search_and_load()
    TTSTest(_config).run()
