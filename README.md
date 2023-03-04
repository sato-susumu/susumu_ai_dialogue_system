# AI音声対話サンプル

ゼロから作るよりも簡単じゃないですかねという程度のサンプル

[![紹介動画](https://user-images.githubusercontent.com/75652942/222885020-d49fd936-dd42-456f-8dd1-a0f6c796748c.jpg)](https://www.youtube.com/watch?v=If8LfBJkAtQ)



## できること

- ChatGPTを使ったボイスチャット、テキストチャット

- ParlAIを使ったボイスチャット、テキストチャット

- 音声認識や音声合成のモジュールを入れ替えて実行

- OBSを使った字幕表示

## できてないこと

- 様々なエラー処理

- いろいろ

## サンプル一覧

| ソースコード                                 | チャットモジュール | 音声認識                      | 音声出力     | 翻訳          | 字幕  |
|----------------------------------------|-----------|---------------------------|----------|-------------|-----|
| chatgpt_text_chat_sample.py            | ChatGPT   | 標準入力 [^1]                 | -        | -           | -   |
| chatgpt_voice_chat_sample.py           | ChatGPT   | SpeechRecognition(Google) | pyttsx3  | -           | -   |
| chatgpt_voice_chat_sample2.py          | ChatGPT   | Googleストリーミング音声認識         | VOICEVOX | -           | -   |
| chatgpt_voice_chat_sample2_with_obs.py | ChatGPT   | Googleストリーミング音声認識         | VOICEVOX | -           | OBS |
| parlai_text_chat_sample.py             | ParlAI    | 標準入力 [^1]                 | -        | Googletrans | -   |
| parlai_voice_chat_sample.py            | ParlAI    | SpeechRecognition(Google) | pyttsx3  | Googletrans | -   |
| parlai_voice_chat_sample2.py           | ParlAI    | Googleストリーミング音声認識         | VOICEVOX | DeepL       | -   |

[^1]: 音声認識モジュールのインタフェースに合わせた擬似的な音声認識モジュール

## 対応モジュール

同じカテゴリのモジュールは簡単に入れ替えることができます。

| カテゴリ | モジュール | 条件        |
| -------- | ---------- | ------------------ |
| チャット | ChatGPT    | APIキー必要 |
| チャット     | ParlAI | ParlAIチャットサーバー必要 |
| 音声認識 | Googleストリーミング音声認識 | Googleの認証必要 |
| 音声認識 | SpeechRecognition(Google) |  |
| 音声認識 | 標準入力を使った擬似的な音声認識 |  |
| 音声合成 | VOICEVOX | VOICEVOXサーバーまたはアプリの起動が必要 |
| 音声合成 | Google音声合成 | Googleの認証必要 |
| 音声合成 | pyttsx3 |  |
| 音声合成 | gtts |  |
| 翻訳 | Googletrans |  |
| 翻訳 | DeepL | APIキー必要 |

## 実行手順

### 関連パッケージのインストール

```
pip install -U -r requirements.txt
```

### config/config.yamlを作成

1. config/sample_config.yaml をコピーする。
2. コピーしたファイル名をconfig/config.yamlにする。
3. config/config.yamlの中身を必要に応じて編集する。
4. ChatGPTを使う場合は、openai_api_keyの内容を変更する。

### サンプルを実行する

#### ChatGPTを使った簡易ボイスチャットの場合

1. コマンドラインでPythonスクリプトを実行する
    ```
    python samples/chatgpt_voice_chat_sample.py
    ```

#### ChatGPTを使ったリッチなボイスチャットの場合

ストリーミング音声認識、VOICEVOXによる音声合成を使うので簡易ボイスチャットよりもリッチです。

1. VOICEVOXアプリの起動する  
   音声合成にVOICEVOXサーバーが必要になります。  
   VOICEVOXアプリにはサーバー機能も含まれているのでアプリを立ち上げればOKです。
2. Googleの認証を設定する
    ```
    gcloud auth ほにゃらら 覚えてないです
    ```
3. コマンドラインでPythonスクリプトを実行する
    ```
    python samples/chatgpt_voice_chat_sample2.py
    ```

## 動作確認環境

Windows 11

Python 3.10



