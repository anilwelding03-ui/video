from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Ensure models are imported so SQLAlchemy registers them on metadata.
from app.models.job import Job  # noqa: E402,F401
from app.models.project import Project  # noqa: E402,F401
from app.models.scene import Scene  # noqa: E402,F401
from app.models.shot import Shot  # noqa: E402,F401
