import loguru
import numpy as np
import requests
import json

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.base_emotion_model import BaseEmotionModel
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


# noinspection PyMethodMayBeStatic
class WrimeEmotionClient(BaseEmotionModel):
    def __init__(self, config: Config):
        super().__init__(config)

    def get_max_emotion(self, text: str) -> (Emotion, float, dict):
        result_dict, raw_dict = self.get_emotion(text)
        max_emotion = max(result_dict, key=result_dict.get)
        return max_emotion, result_dict[max_emotion], result_dict

    def get_emotion(self, text: str) -> (dict, dict):
        result_dict = self.get_raw_emotion(text)
        return self._convert_emotion_dict(result_dict), result_dict

    def _convert_emotion_dict(self, in_dict: dict):
        out_dict = {
            Emotion.HAPPY: max(in_dict.get('Joy'), in_dict.get('Trust')),
            Emotion.SAD: max(in_dict.get('Sadness'), in_dict.get('Fear')),
            Emotion.SURPRISED: in_dict.get('Surprise'),
            Emotion.ANGRY: in_dict.get('Anger'),
            Emotion.RELAXED: 0.0,
        }
        return out_dict

    def _np_softmax(self, x):
        f_x = np.exp(x) / np.sum(np.exp(x))
        return f_x

    def get_raw_emotion(self, text: str) -> dict:
        request_dic = {'text': text}
        request_json = json.dumps(request_dic)

        host = self._config.get_wrime_emotion_server_host()
        port_no = self._config.get_wrime_emotion_server_port_no()
        # noinspection HttpUrlsUsage
        url = f"http://{host}:{port_no}/analyze_emotion"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=request_json, headers=headers)
        response_json = response.json()

        return response_json["emotions"]


if __name__ == '__main__':

    _config = Config()
    _model = WrimeEmotionClient(_config)

    def func(text: str):
        out_dict, raw_dict = _model.get_emotion(text)
        max_key = max(out_dict, key=out_dict.get)
        max_value = out_dict[max_key]
        loguru.logger.debug(text)
        loguru.logger.debug(raw_dict)
        loguru.logger.debug(out_dict)
        loguru.logger.debug(f"max_key: {max_key}, max_value: {max_value}")
        loguru.logger.debug("")


    func("大好きな人が遠くへ行ってしまった")
    func("誰がこんなことをしたんだ！？もう許せない。")
    func("いい加減にしてくれ！もう限界だ！")
    func("何度も言ってるのに、何も聞いてくれない。もう腹が立つ！")
    func("喧嘩したけど仲直りできた！")
    func("友達と喧嘩した。泣きそう。")
    func("我慢せずに食べまくる。倍返しだ。")
    func("好きなアーティストのコンサートだったのに。。。")
    func("私が立ち上がった時、世界は回っていると思った。後で気がついたら、私が回っていたのだとわかった。")
    func('もう怒った!')
    func('ああ、もうやだ')
    func('頼りになりますね！')
