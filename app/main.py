import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.commons.logger import setup_logger
from app.commons.middleware.logger_middleware import LoggerMiddleware

from .routers.base import router as base_routers
from .routers.v1 import router as v1_router

setup_logger()
LOGGER = logging.getLogger(__name__)

app = FastAPI(
    title="Origin Financial SWE Challenge",
    description="Matheus Mansour's Contestant Solution",
)

app.add_middleware(LoggerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(base_routers)
app.include_router(v1_router)
