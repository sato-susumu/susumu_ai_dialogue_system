import pytest
from unittest.mock import patch, MagicMock
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.wrime_emotion_client import WrimeEmotionClient
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


class TestWrimeEmotionClient:
    @pytest.fixture(scope='module')
    def config(self):
        return Config()

    @pytest.fixture(scope='module')
    def client(self, config):
        return WrimeEmotionClient(config)

    @patch('requests.post')
    def test_get_raw_emotion(self, mock_post, client):
        response_json = {
            'emotions': {'Joy': 0.3, 'Trust': 0.2, 'Sadness': 0.1, 'Fear': 0.4, 'Anger': 0.0, 'Surprise': 0.0}}
        mock_post.return_value = MagicMock(json=lambda: response_json)

        result = client.get_raw_emotion('test')

        assert result == response_json['emotions']
        mock_post.assert_called_once_with(
            'http://127.0.0.1:56563/analyze_emotion',
            data='{"text": "test"}',
            headers={'Content-Type': 'application/json'}
        )

    def test_convert_emotion_dict(self, client):
        in_dict = {'Joy': 0.3, 'Trust': 0.2, 'Sadness': 0.1, 'Fear': 0.4, 'Anger': 0.0, 'Surprise': 0.0}
        out_dict = {
            Emotion.HAPPY: 0.3,
            Emotion.SAD: 0.4,
            Emotion.SURPRISED: 0.0,
            Emotion.ANGRY: 0.0,
            Emotion.RELAXED: 0.0,
        }
        result = client._convert_emotion_dict(in_dict)

        assert result == out_dict

    @patch.object(WrimeEmotionClient, 'get_raw_emotion')
    def test_get_emotion(self, mock_get_raw_emotion, client):
        raw_dict = {'Joy': 0.3, 'Trust': 0.2, 'Sadness': 0.1, 'Fear': 0.4, 'Anger': 0.0, 'Surprise': 0.0}
        mock_get_raw_emotion.return_value = raw_dict

        out_dict = {
            Emotion.HAPPY: 0.3,
            Emotion.SAD: 0.4,
            Emotion.SURPRISED: 0.0,
            Emotion.ANGRY: 0.0,
            Emotion.RELAXED: 0.0,
        }
        result = client.get_emotion('test')

        assert result == (out_dict, raw_dict)

    @patch.object(WrimeEmotionClient, 'get_emotion')
    def test_get_max_emotion(self, mock_get_emotion, client):
        result_dict = {
            Emotion.HAPPY: 0.3,
            Emotion.SAD: 0.4,
            Emotion.SURPRISED: 0.0,
            Emotion.ANGRY: 0.0,
            Emotion.RELAXED: 0.0,
        }
        mock_get_emotion.return_value = (result_dict, {})

        result = client.get_max_emotion('test')
        assert result[0] == Emotion.SAD
        assert result[1] == 0.4
        assert result[2] == result_dict
