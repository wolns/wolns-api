from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.core.lifespan import lifespan
from src.core.server import Server
from . import models
from . import tasks


def create_app(_=None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    Instrumentator().instrument(app).expose(app)
    return Server(app).get_app()
