from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import exports, health, pipeline, projects
from app.db.base import Base
from app.db.session import engine
from app.services.project_store import ensure_data_directories

app = FastAPI(title="Video Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(projects.router)
app.include_router(pipeline.router)
app.include_router(exports.router)


@app.on_event("startup")
def on_startup() -> None:
    ensure_data_directories()
    Base.metadata.create_all(bind=engine)
