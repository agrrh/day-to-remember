from typing import Annotated
from uuid import UUID, uuid4

from pydantic import AfterValidator, BaseModel, Field


class User(BaseModel):
    uuid: Annotated[str, AfterValidator(lambda x: UUID(x, version=4))] = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""
    telegram_id: int = 0
