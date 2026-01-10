import datetime
from typing import Annotated, Any, Literal, override
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.errors import DomainError
from app.domain.review_period import ReviewPeriodScope


class ErrorFactTextEmpty(DomainError):
    """Fact must have some sane text."""


class ErrorFactUnexpectedType(DomainError):
    """Fact field has unexpected type."""


class Fact(BaseModel):
    """Event happened at particular day."""

    uuid: Annotated[str, UUID] = Field(default_factory=lambda: str(uuid4()))

    user_uuid: Annotated[str, UUID]
    text: str
    date: datetime.date = Field(default_factory=datetime.datetime.today)

    selected_at_scope: ReviewPeriodScope | Literal[""] | None = None

    # TODO: Add FactStored
    # FIXME: selected_at_scope should not include "", this should go to FactStored
    # TODO: Adopt createdAt and updatedAt, but in snake_case

    @override
    def model_post_init(self, context: Any) -> None:
        if not self.text or len(self.text) < 10:
            raise ErrorFactTextEmpty

        if not isinstance(self.date, datetime.date):
            raise ErrorFactUnexpectedType
