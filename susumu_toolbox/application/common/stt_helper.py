from typing import Optional

from susumu_toolbox.infrastructure.config import Config, InputFunction


class STTHelper:
    def __init__(self, config: Config):
        self._config = config

    def get_start_message_for_console(self) -> Optional[str]:
        stt = self._config.get_common_input_function()
        match stt:
            case InputFunction.SR_GOOGLE | InputFunction.WHISPER_API:
                return "マイクに向かって何か５文字以上話しかけてください"
            case InputFunction.GOOGLE_STREAMING:
                return "マイクに向かって何か話しかけてください"
            case InputFunction.STDIN_PSEUD:
                return "このウィンドウに発言を入力してリターンを押してください。終了する場合はbyeと入力"
            case InputFunction.YOUTUBE_PSEUD:
                return "YouTubeライブチャットのコメント取得開始"
            case _:
                raise ValueError(f"Invalid input_function: {stt}")

    def get_start_message_for_caption(self) -> Optional[str]:
        stt = self._config.get_common_input_function()
        match stt:
            case InputFunction.SR_GOOGLE | InputFunction.WHISPER_API:
                return "(マイクに向かって何か５文字以上話しかけてください)"
            case InputFunction.GOOGLE_STREAMING:
                return "(マイクに向かって何か話しかけてください)"
            case InputFunction.STDIN_PSEUD:
                return "(メッセージ入力待ち)"
            case InputFunction.YOUTUBE_PSEUD:
                return None
            case _:
                raise ValueError(f"Invalid input_function: {stt}")

