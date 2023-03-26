from multiprocessing import Value
from threading import Timer
from typing import Optional

# noinspection PyPackageRequirements
from google.cloud import speech

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.stt.base_stt import BaseSTT, STTResult, MicrophoneStream, STTEvent


# noinspection PyMethodMayBeStatic
class GoogleStreamingSTT(BaseSTT):
    _SILENCE_TIMEOUT_SECOND = 3.0
    _SAMPLING_RATE = 16000
    _CHUNK_SIZE = int(_SAMPLING_RATE / 10)  # 100ms

    def __init__(self, config: Config, language_code: str = "ja-JP", single_utterance: bool = True,
                 speech_contexts: Optional[list[str]] = None):
        super().__init__(config)
        self._timed_out = Value('i', 0)
        self._transcript = ""
        self._language_code = language_code
        self._single_utterance = single_utterance
        self._stream = None
        # noinspection PyBroadException
        try:
            self._client = speech.SpeechClient()
        except Exception:
            api_key = self._config.get_gcp_speech_to_text_api_key()
            self._client = speech.SpeechClient(client_options={"api_key": api_key})
        self._streaming_config = self._get_streaming_config(speech_contexts or [])

    def _get_streaming_config(self, speech_contexts: list[str]):
        # Add the hard-coded leaf-node commands
        contexts = [speech.SpeechContext(phrases=speech_contexts)]  # noqa

        config = speech.RecognitionConfig(
            # 非圧縮の 16 ビット符号付きリトル エンディアン サンプル (リニアPCM)
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # noqa
            sample_rate_hertz=self._SAMPLING_RATE,  # noqa
            language_code=self._language_code,  # noqa
            # model="command_and_search",  # noqa
            speech_contexts=contexts,  # noqa
        )

        return speech.StreamingRecognitionConfig(
            config=config,  # noqa
            # 中間結果を返すかどうか
            interim_results=True,  # noqa
            # 1回だけ音声認識するかどうか。音声コマンド向け。終話検出が早いような気がする。(未検証)
            single_utterance=self._single_utterance  # noqa
        )

    def _on_timeout(self):
        with self._timed_out.get_lock():
            self._timed_out.value = 1
        if self._stream:
            self._stream.close()
            self._stream = None
        self._event_publish(STTEvent.RESULT, STTResult(self._transcript, True, True))

    def _processing(self, response_generator):
        timer = None
        self._transcript = ""
        with self._timed_out.get_lock():
            self._timed_out.value = 0
        try:
            for response in response_generator:
                if self._timed_out.value == 1:
                    break

                self._event_publish(STTEvent.DEBUG_MESSAGE, response)
                if not response.results:
                    if self._single_utterance:
                        if response.speech_event_type.name == "END_OF_SINGLE_UTTERANCE":
                            # single_utterance=Trueの場合、次のような挙動になる
                            # ・END_OF_SINGLE_UTTERANCEを返したあと、ワンテンポ遅れてis_final=Trueで認識結果が返る
                            # ・END_OF_SINGLE_UTTERANCEを返すものの、その後無反応になることがある。(主に無音の場合)
                            #
                            # 無反応対策でタイマーを使って監視
                            timer = Timer(self._SILENCE_TIMEOUT_SECOND, self._on_timeout)
                            timer.start()
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                self._transcript = result.alternatives[0].transcript

                if result.is_final:
                    self._event_publish(STTEvent.RESULT, STTResult(self._transcript, True))
                    if self._single_utterance:
                        break
                else:
                    # is_final=Falseで返ってきた結果は認識精度が低いため、表示以外の用途で使うのはオススメできない。
                    # 不鮮明な音だと is_final=False で何度か結果が返ってくるものの、その後何も反応がないことがある。
                    self._event_publish(STTEvent.RESULT, STTResult(self._transcript, False))
        finally:
            if timer:
                timer.cancel()

    @BaseSTT.recognize_decorator
    def recognize(self):
        with MicrophoneStream(self._SAMPLING_RATE, self._CHUNK_SIZE) as stream:
            self._recognize(stream)

    def _recognize(self, audio_stream=None):
        self._stream = audio_stream
        audio_generator = self._stream.generator()
        audio_generator_object = (
            speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator  # noqa
        )

        self._event_publish(STTEvent.START)
        # ストリーミング認識。何か返すべきものがあるまでブロッキング
        # メソッドの詳細は下記参照
        # https://cloud.google.com/python/docs/reference/speech/latest/google.cloud.speech_v1.services.speech.SpeechClient#google_cloud_speech_v1_services_speech_SpeechClient_streaming_recognize
        response_generator = self._client.streaming_recognize(self._streaming_config, audio_generator_object)  # noqa

        self._processing(response_generator)
        self._stream = None
