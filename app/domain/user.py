from typing import Annotated
from uuid import UUID, uuid4

from pydantic import AfterValidator, BaseModel, Field


class User(BaseModel):
    """User container."""

    uuid: Annotated[str, AfterValidator(lambda x: str(UUID(x)))] = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""
    telegram_id: int = 0

    # TODO: Add UserStored
    # TODO: Adopt createdAt and updatedAt, but in snake_case
