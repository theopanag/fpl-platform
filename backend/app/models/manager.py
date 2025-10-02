"""
Manager database model.

Represents FPL managers and their basic information.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.gameweek import Gameweek
    from app.models.league import League


class Manager(Base):
    """Manager model for storing FPL manager information."""

    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fpl_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    player_first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    player_last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    player_region_name: Mapped[str] = mapped_column(String(255), nullable=False)
    player_region_id: Mapped[int] = mapped_column(Integer, nullable=False)
    player_region_short_iso: Mapped[str] = mapped_column(String(10), nullable=False)
    summary_overall_points: Mapped[int] = mapped_column(Integer, default=0)
    summary_overall_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    summary_event_points: Mapped[int] = mapped_column(Integer, default=0)
    summary_event_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_event: Mapped[int] = mapped_column(Integer, default=1)
    total_transfers: Mapped[int] = mapped_column(Integer, default=0)

    # League association
    league_id: Mapped[int | None] = mapped_column(
        ForeignKey("leagues.id"), nullable=True
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    league: Mapped["League"] = relationship("League", back_populates="managers")
    gameweeks: Mapped[list["Gameweek"]] = relationship(
        "Gameweek", back_populates="manager"
    )

    @property
    def full_name(self) -> str:
        """Get manager's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def player_full_name(self) -> str:
        """Get player's full name."""
        return f"{self.player_first_name} {self.player_last_name}"

    def __repr__(self) -> str:
        return f"<Manager(id={self.id}, name='{self.full_name}', fpl_id={self.fpl_id})>"