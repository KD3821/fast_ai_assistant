from datetime import datetime

from fastapi import Request

from src.logger import logger


async def logging_middleware(request: Request, call_next):
    logging_data = {
        "method": request.method,
        "date": datetime.utcnow(),
        "url": request.url.path,
        "query_params": request.query_params,
        "client": request.scope.get("client"),
        "referer": request.headers.get("referer"),
        "user-agent": request.headers.get("user-agent"),
    }
    logging_string = " | ".join([f'"{str(value)}"' for value in logging_data.values()])
    logger.info(logging_string)
    response = await call_next(request)
    return response
