import uuid

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from src.connectors import TravelConnector
from src.schemas.prompt import PromptRequest, PromptResponse
from src.service import agent

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.get("/session-id")
async def get_session():
    return {"session_id": str(uuid.uuid4().hex)}


@router.post("/travel-agent")
async def travel_agent_chat(prompt: PromptRequest) -> PromptResponse:
    return await agent.assist_travel(query=prompt.input, session_id=prompt.session_id)


@router.websocket("/travel-chat")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str = Query(default=None),
    connector: TravelConnector = Depends(),
):
    if session_id is None:
        session_id = str(uuid.uuid4().hex)
    await websocket.accept(headers=[("session_id".encode(), session_id.encode())])
    await connector.bind(session_id, websocket)
    try:
        while True:
            message = await websocket.receive_json()
            await connector.process_query(
                query=message.get("text"), session_id=message.get("session_id")
            )
    except WebSocketDisconnect:
        await connector.release(session_id)
