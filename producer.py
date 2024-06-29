import asyncio
import json
from typing import Any, Dict

import aio_pika

from src.settings import fast_ai_settings

__all__ = ["broker_producer"]


class Producer:
    connection: aio_pika.abc.AbstractRobustConnection = None
    channel: aio_pika.abc.AbstractChannel = None
    response_queue: aio_pika.abc.AbstractQueue = None
    answers: Dict[str, asyncio.Future] = dict()

    def __init__(self, amqp_dsn: str, service_name: str):
        self.amqp_dsn = amqp_dsn
        self.service_name = service_name

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.amqp_dsn)
        self.channel = await self.connection.channel()
        self.response_queue = await self.channel.declare_queue(
            f"{self.service_name}_responses", durable=True
        )
        await self.response_queue.consume(self.consume)

    async def consume(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        session_id = message.correlation_id
        answer = self.answers.get(session_id, None)
        if answer:
            answer.set_result(json.loads(message.body.decode("utf-8")))
        await message.ack()

    async def request(self, *, session_id: str, to: str, payload: dict):
        self.answers[session_id] = asyncio.Future()
        message = aio_pika.message.Message(
            body=json.dumps(payload).encode("utf-8"),
            correlation_id=session_id,
            reply_to=self.response_queue.name,
        )
        await self.channel.default_exchange.publish(message, routing_key=to)
        return await self.answers[session_id]

    async def process_request(
        self, session_id: str, service_name: str, data: Dict[str, Any]
    ) -> asyncio.Future:
        return await self.request(session_id=session_id, to=f"{service_name}_requests", payload=data)


broker_producer = Producer(
    str(fast_ai_settings.amqp_dsn), fast_ai_settings.service_name
)
