from samples.chatgpt_voice_chat_sample2 import ChatGPTVoiceChatSample2
from susumu_toolbox.utility.config import Config

if __name__ == "__main__":
    _config = Config()
    _config.load()
    ChatGPTVoiceChatSample2(_config).run_forever()
