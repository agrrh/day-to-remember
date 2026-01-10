from enum import Enum
from typing import Annotated, List
from uuid import UUID, uuid4

from pydantic import AfterValidator, BaseModel, Field, Json

from app.domain.fact import Fact
from app.domain.review_period import (
    ReviewPeriod,
    # ReviewPeriodMonth,
    ReviewPeriodScope,
    # ReviewPeriodWeek,
)
from app.domain.user import User

# from app.infrastructure.repositories.fact import FactRepository
# from app.infrastructure.repositories.review_session import ReviewSessionRepository
# from app.infrastructure.repositories.user import UserRepository


class ReviewSessionStatus(str, Enum):
    """Possible states of ReviewSession.

    - Created
    - Collected - Facts gathered
    - Notified - recieved by User
    - Completed - choice of important task has been made
    """

    CREATED = "created"
    COLLECTED = "collected"
    NOTIFIED = "notified"
    COMPLETED = "completed"


class ReviewSessionStored(BaseModel):
    """Database representation of ReviewSession."""

    uuid: Annotated[str, AfterValidator(lambda x: str(UUID(x)))]

    user_uuid: Annotated[str, AfterValidator(lambda x: str(UUID(x)))]
    period_scope: ReviewPeriodScope
    date_start: float  # unix timestamp
    date_end: float  # unix timestamp
    fact_uuids: Json[List[Annotated[str, AfterValidator(lambda x: str(UUID(x)))]]]
    status: ReviewSessionStatus
    selected_fact_uuid: (
        Annotated[str, AfterValidator(lambda x: str(UUID(x)))] | None
    ) = None

    # @override
    # def model_post_init(self, context: Any) -> None:
    #     if not self.text or len(self.text) < 10:
    #         raise ErrorFactTextEmpty


class ReviewSession(BaseModel):
    """Aggregate to represent Facts for given Period and their state.

    Also uuid of most important Fact, if selected.
    """

    uuid: Annotated[str, AfterValidator(lambda x: str(UUID(x)))] = Field(
        default_factory=lambda: str(uuid4())
    )

    user: User
    period: ReviewPeriod

    status: ReviewSessionStatus = ReviewSessionStatus.CREATED

    facts: List[Fact] = Field(default_factory=list)
    selected_fact: Fact | None = None

    # def load_stored(
    #     self,
    #     stored: ReviewSessionStored,
    #     user_repository: UserRepository,
    #     rs_repository: ReviewSessionRepository,
    #     fact_repository: FactRepository,
    # ):
    #     """Load object from database representation."""
    #     self.uuid = stored.uuid
    #     self.user = user_repository.get_by_uuid(stored.user_uuid)

    #     period_class = {
    #         ReviewPeriodScope.WEEK: ReviewPeriodWeek,
    #         ReviewPeriodScope.MONTH: ReviewPeriodMonth,
    #     }.get(stored.period_scope)

    #     if period_class is None:
    #         raise ValueError

    #     self.period = period_class(
    #         start=stored.date_start,
    #         end=stored.date_end,
    #     )

    #     self.status = stored.status
    #     self.facts = [fact_repository.get_by_uuid(_) for _ in stored.fact_uuids]

    #     if stored.selected_fact_uuid:
    #         self.selected_fact = fact_repository.get_by_uuid(stored.selected_fact_uuid)
