from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Shot(Base):
    __tablename__ = "shots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey("scenes.id", ondelete="CASCADE"), nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt_master: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_negative: Mapped[str] = mapped_column(Text, default="", nullable=False)
    duration_s: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)

    scene = relationship("Scene", back_populates="shots")
