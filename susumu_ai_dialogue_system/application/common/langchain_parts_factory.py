from langchain import OpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory, ConversationSummaryMemory, \
    ConversationSummaryBufferMemory, CombinedMemory

from susumu_ai_dialogue_system.infrastructure.config import Config, LangChainMemoryType


class LangChainPartsFactory:

    @staticmethod
    def create_memory(config: Config):
        memory_type = config.get_langchain_memory_type()
        match memory_type:
            case LangChainMemoryType.ConversationBufferMemory:
                return ConversationBufferMemory(return_messages=True)
            case LangChainMemoryType.ConversationBufferWindowMemory:
                return ConversationBufferWindowMemory(k=10, return_messages=True)
            case LangChainMemoryType.ConversationSummaryMemory:
                return ConversationSummaryMemory(llm=OpenAI(), input_key="input", return_messages=True)
            case LangChainMemoryType.ConversationSummaryBufferMemory:
                return ConversationSummaryBufferMemory(llm=OpenAI(), max_token_limit=40, return_messages=True)
            case LangChainMemoryType.CombinedMemory:
                conv_memory = ConversationBufferWindowMemory(k=10, return_messages=True)
                summary_memory = ConversationSummaryMemory(llm=OpenAI(), input_key="input",
                                                           return_messages=True)
                return CombinedMemory(memories=[conv_memory, summary_memory])
            case _:
                raise ValueError(f"Invalid memory_type: {memory_type}")
