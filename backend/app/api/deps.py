"""
API dependencies for dependency injection.

Common dependencies used across API endpoints.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

# Database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_db)]