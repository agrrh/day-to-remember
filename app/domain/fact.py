from pydantic import BaseModel, Field

from uuid import uuid4
import datetime

from app.domain.errors import DomainError


class ErrorFactTextEmpty(DomainError):
    """Fact must have some sane text."""


class Fact(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))

    user_uuid: str  # TODO: Validate as uuid
    text: str
    date: datetime.date = Field(default_factory=datetime.datetime.today)

    # TODO: Place validation rules to more conventional place
    def create(self):
        if not self.text or len(self.text) < 10:
            raise ErrorFactTextEmpty
