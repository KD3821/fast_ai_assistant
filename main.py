import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.producer import broker_producer
from src.consumer import broker_consumer
from src.settings import fast_ai_settings
from src.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.gather(
        broker_producer.connect(),
        broker_consumer.connect()
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Fast AI Assistant",
    description="AI Travel Agent",
    version="1.0.1",
)

app.include_router(router)

allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=fast_ai_settings.server_host,
        port=fast_ai_settings.server_port,
        reload=False
    )
