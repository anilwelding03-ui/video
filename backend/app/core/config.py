from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "backend" / "app" / "data"
PROJECTS_DIR = DATA_DIR / "projects"
SQLITE_DB_PATH = DATA_DIR / "app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
