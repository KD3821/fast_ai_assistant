from langchain_openai import ChatOpenAI
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_openai_tools_agent

from src.settings import fast_ai_settings


__all__ = ["ai_model"]


class LLM:
    def __init__(self, llm_model: str):
        self.chat = ChatOpenAI(model_name=llm_model, openai_api_key=fast_ai_settings.openai_api_key, temperature=0)

    def init_travel_agent(self, prompt_template, tools):
        agent = create_openai_tools_agent(self.chat, tools, prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: MongoDBChatMessageHistory(
                database_name=fast_ai_settings.db_name,
                collection_name="history",
                connection_string=f"mongodb://{fast_ai_settings.db_host}:27017",
                session_id=session_id
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history


ai_model = LLM(llm_model=fast_ai_settings.llm_model)


# chat: ChatOpenAI | None = None
# agent_with_chat_history: RunnableWithMessageHistory | None = None
#
#
# def LLM_init():
#     global chat, agent_with_chat_history
#     chat = ChatOpenAI(model_name=fast_ai_settings.llm_model, temperature=0)
#     tools = [agent_tools.vacation_lookup, agent_tools.itinerary_lookup, agent_tools.book_cruise]
#
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "You are a helpful and friendly travel assistant for a cruise company. Answer travel questions to "
#                 "the best of your ability providing only relevant information. In order to book a cruise you will "
#                 "need to capture the person's name.",
#             ),
#             MessagesPlaceholder(variable_name="chat_history"),
#             ("user", "{input}"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )
#
#     # Answer should be embedded in html tags. Only answer questions related to cruise travel, If you can not answer
#     # respond with \"I am here to assist with your travel questions.\".
#     # Removed: Answer should be embedded in html tags. {input}
#
#     agent = create_openai_tools_agent(chat, tools, prompt)
#     agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
#
#     agent_with_chat_history = RunnableWithMessageHistory(
#         agent_executor,
#         lambda session_id: MongoDBChatMessageHistory(
#             database_name=fast_ai_settings.db_name,
#             collection_name="history",
#             connection_string=f"mongodb://{fast_ai_settings.db_host}:27017",
#             session_id=session_id
#         ),
#         input_messages_key="input",
#         history_messages_key="chat_history",
#     )
#
#
# LLM_init()
