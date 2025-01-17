import asyncio
from datetime import datetime
from typing import Dict

from fastapi import WebSocket, WebSocketException, status

from src.logger import logger
from src.producer import broker_producer
from src.settings import fast_ai_settings


class TravelConnector:
    __active_connections: Dict[str, WebSocket] = dict()

    def __init__(self):
        self.__dict__ = self.__active_connections

    async def bind(self, session_id: str, websocket: WebSocket) -> None:
        self.__dict__[session_id] = websocket
        await asyncio.to_thread(
            logger.info,
            f"{datetime.utcnow()}: BINDING WS conn for [{session_id=}]"
        )

    async def release(self, session_id: str, websocket: WebSocket) -> None:
        if self.__dict__.get(session_id) == websocket:
            self.__dict__.pop(session_id)
            await asyncio.to_thread(
                logger.info,
                f"{datetime.utcnow()}: RELEASING WS conn for [{session_id=}]"
            )
        else:
            await asyncio.to_thread(
                logger.info,
                f"{datetime.utcnow()}: IGNORING previous WS conn for [{session_id=}]"
            )

    async def reply(self, answer: dict, session_id: str):
        if (ws := self.__dict__.get(session_id)) is not None and broker_producer.answers.get(session_id) is not None:
            broker_producer.answers.pop(session_id)
            await ws.send_json(
                {
                    "text": answer.get("result").get("text"),
                    "seconds": answer.get("result").get("seconds"),
                }
            )

    async def process_query(self, *, query: str, session_id: str) -> None:
        if self.__dict__.get(session_id) is None:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION, reason="SessionID Not Found"
            )
        answer = await broker_producer.process_request(
            session_id=session_id,
            service_name=f"{fast_ai_settings.service_name}",
            data={"query": query, "session_id": session_id},
        )
        await self.reply(answer, session_id)

    async def restore_answer(self, session_id: str) -> None:
        query_task = broker_producer.answers.get(session_id)
        await asyncio.to_thread(
            logger.info,
            f"{datetime.utcnow()}: RESTORING WS conn for [{session_id=}] with {query_task=}"
        )
        if query_task is not None:
            if not query_task.done():
                answer = await query_task
            else:
                answer = query_task.result()
            await self.reply(answer, session_id)
