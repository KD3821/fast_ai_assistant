from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

cruise_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly travel assistant for a cruise company. Answer travel questions to "
            "the best of your ability providing only relevant information. In order to book a cruise you will "
            "need to capture the person's name.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
