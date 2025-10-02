"""
League database model.

Represents FPL leagues and their metadata.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.manager import Manager


class League(Base):
    """League model for storing FPL league information."""

    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fpl_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    league_type: Mapped[str] = mapped_column(String(50), nullable=False)
    scoring: Mapped[str] = mapped_column(String(50), nullable=False)
    admin_entry: Mapped[int | None] = mapped_column(Integer, nullable=True)
    start_event: Mapped[int] = mapped_column(Integer, nullable=False)
    code_privacy: Mapped[str] = mapped_column(String(50), nullable=False)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    managers: Mapped[list["Manager"]] = relationship(
        "Manager", back_populates="league"
    )

    def __repr__(self) -> str:
        return f"<League(id={self.id}, name='{self.name}', fpl_id={self.fpl_id})>"