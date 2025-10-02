"""
Gameweek database model.

Represents gameweek performance data for managers.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.manager import Manager


class Gameweek(Base):
    """Gameweek model for storing manager performance data."""

    __tablename__ = "gameweeks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), nullable=False)
    event: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rank_sort: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bank: Mapped[int] = mapped_column(Integer, default=0)
    value: Mapped[int] = mapped_column(Integer, default=0)
    event_transfers: Mapped[int] = mapped_column(Integer, default=0)
    event_transfers_cost: Mapped[int] = mapped_column(Integer, default=0)
    points_on_bench: Mapped[int] = mapped_column(Integer, default=0)

    # Team selection data (JSON fields)
    picks: Mapped[dict] = mapped_column(JSON, nullable=True)
    automatic_subs: Mapped[list] = mapped_column(JSON, nullable=True)
    entry_history: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    manager: Mapped["Manager"] = relationship("Manager", back_populates="gameweeks")

    def __repr__(self) -> str:
        return f"<Gameweek(id={self.id}, manager_id={self.manager_id}, event={self.event}, points={self.points})>"