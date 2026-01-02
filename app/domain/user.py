from pydantic import BaseModel, Field
from uuid import uuid4


class User(BaseModel):
    # TODO: Validate as uuid
    uuid: str = Field(default_factory=lambda: str(uuid4()))

    name: str = ""
    telegram_id: int = 0
