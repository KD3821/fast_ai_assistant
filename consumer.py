import json
from typing import Callable

import aio_pika

from src.settings import fast_ai_settings
from src.service import agent

__all__ = ["broker_consumer"]


class Consumer:
    connection: aio_pika.abc.AbstractRobustConnection = None
    channel: aio_pika.abc.AbstractChannel = None
    request_queue: aio_pika.abc.AbstractQueue = None

    def __init__(self, amqp_dsn: str, service_name: str, consumer_callback: Callable):
        self.amqp_dsn = amqp_dsn
        self.service_name = service_name
        self.consumer_callback = consumer_callback

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.amqp_dsn)
        self.channel = await self.connection.channel()
        self.request_queue = await self.channel.declare_queue(
            f"{self.service_name}_requests", durable=True
        )
        await self.request_queue.consume(self.consume)

    async def consume(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        msg = json.loads(message.body.decode("utf-8"))
        result = self.consumer_callback(**msg)
        await self.response(
            to=message.reply_to,
            correlation_id=message.correlation_id,
            payload={"result": result.model_dump()}
        )
        await message.ack()

    async def response(self, *, to: str, correlation_id: str, payload: dict):
        message = aio_pika.message.Message(
            body=json.dumps(payload).encode("utf-8"),
            correlation_id=correlation_id
        )
        await self.channel.default_exchange.publish(message, routing_key=to)


broker_consumer = Consumer(
    str(fast_ai_settings.amqp_dsn), fast_ai_settings.service_name, agent.assist_travel
)
