import asyncio
import os
import sys

import aio_pika
import uvicorn
from fastapi import FastAPI

# from currency_service.src.infrastructure.api.api_v1.currency import router as currency_router
from currency_service.src.infrastructure.api.handlers.currency_api_handler import start_server
# from currency_service.src.infrastructure.config.logging_config import LoggingConfig
# from currency_service.src.infrastructure.config.rmq_config import RMQ_HOST, RMQ_PORT, RMQ_USER, RMQ_PASSWORD

# app = FastAPI()
# app.include_router(currency_router)
#
#
# @app.on_event("startup")
# async def startup():
#     logger = LoggingConfig().get_logger()
#     logger.debug("Startup")
#     start_server()


if __name__ == '__main__':
    # uvicorn.run("main:app", reload=True)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    start_server()
