from pathlib import Path

from app.core.config import PROJECTS_DIR


def ensure_data_directories() -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def create_project_directory(project_id: int) -> Path:
    project_dir = PROJECTS_DIR / str(project_id)
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir
