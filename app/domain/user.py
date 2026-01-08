from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    """User container."""

    uuid: Annotated[str, UUID] = Field(default_factory=lambda: str(uuid4()))

    name: str = ""
    telegram_id: int = 0
