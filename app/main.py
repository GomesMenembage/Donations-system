import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.config import settings
from app.database import Base, engine

logger = logging.getLogger(__name__)

app = FastAPI(title="Donations System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.on_event("startup")
def on_startup():
    if settings.is_production:
        logger.warning("Production mode: ensure database migrations are up-to-date (alembic upgrade head)")
    else:
        Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
