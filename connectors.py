from typing import Dict

from fastapi import WebSocket

from src.producer import broker_producer
from src.settings import fast_ai_settings


class TravelConnector:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = dict()

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    async def disconnect(self, websocket: WebSocket):
        for session_id, ws in self.active_connections.items():
            if ws == websocket:
                self.active_connections.pop(session_id)
                break

    async def receive_query(self, session_id: str):
        websocket = self.active_connections.get(session_id)
        message = await websocket.receive_text()

        answer = await broker_producer.process_request(
            session_id=session_id,
            service_name=f"{fast_ai_settings.service_name}",
            data={"query": message, "session_id": session_id}
        )

        text = answer.get('result').get('text')
        seconds = answer.get('result').get('seconds')

        await websocket.send_text(f"[{seconds:.2f} seconds]\n{text}")
