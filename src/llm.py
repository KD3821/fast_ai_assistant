from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI

from src.settings import fast_ai_settings

__all__ = ["ai_model"]


class LLM:
    def __init__(self, llm_model: str):
        self.chat = ChatOpenAI(
            model_name=llm_model,
            openai_api_key=fast_ai_settings.openai_api_key,
            temperature=0,
        )

    def init_travel_agent(self, prompt_template, tools):
        agent = create_openai_tools_agent(self.chat, tools, prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: MongoDBChatMessageHistory(
                database_name=fast_ai_settings.db_name,
                collection_name="history",
                connection_string=f"mongodb://{fast_ai_settings.db_host}:27017",
                session_id=session_id,
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history


ai_model = LLM(llm_model=fast_ai_settings.llm_model)
