from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - registers SQLAlchemy models
from app.routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient for the first local run. We will later replace this with
    # explicit database migrations as part of the deployment workflow.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
Instrumentator().instrument(app).expose(app)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "environment": settings.app_env,
        "status": "running",
    }


@app.get("/health/live", tags=["health"])
def liveness():
    return {"status": "alive"}


@app.get("/health/ready", tags=["health"])
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready", "database": "reachable"}
    except SQLAlchemyError:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "database": "unreachable"},
        )
