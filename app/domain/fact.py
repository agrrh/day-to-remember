import datetime
from typing import Annotated, Any
from uuid import UUID, uuid4

from pydantic import AfterValidator, BaseModel, Field

from app.domain.errors import DomainError


class ErrorFactTextEmpty(DomainError):
    """Fact must have some sane text."""


class Fact(BaseModel):
    uuid: Annotated[str, AfterValidator(lambda x: UUID(x, version=4))] = Field(
        default_factory=lambda: str(uuid4())
    )

    user_uuid: Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    text: str
    date: datetime.date = Field(default_factory=datetime.datetime.today)

    def model_post_init(self, context: Any) -> None:
        if not self.text or len(self.text) < 10:
            raise ErrorFactTextEmpty
