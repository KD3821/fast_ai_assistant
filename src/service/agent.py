import asyncio
import time
from datetime import datetime

from src.llm import ai_model
from src.logger import logger
from src.schemas.prompt import PromptResponse
from src.service import cruise_agent_tools
from src.service.prompt_templates import cruise_prompt


async def assist_travel(*, query: str, session_id: str) -> str:

    travel_ai_agent = ai_model.init_travel_agent(
        prompt_template=cruise_prompt, tools=cruise_agent_tools.tools
    )

    start_time = time.time()

    results = await travel_ai_agent.ainvoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}},
    )

    seconds = time.time() - start_time

    await asyncio.to_thread(
        logger.info,
        f"{datetime.utcnow()}: REPLYING [{session_id=}] query ['{query[:30]}'] processed in [{seconds:.2f}] sec",
    )

    return PromptResponse(text=results.get("output"), seconds=seconds)
