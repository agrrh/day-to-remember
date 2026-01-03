from enum import Enum

from app.domain.fact import Fact
from app.domain.review_period import ReviewPeriod
from app.domain.user import User


class ReviewSessionState(Enum):
    CREATED = "created"
    CHOICE_DONE = "choice_done"


class ReviewSession:
    def __init__(
        self,
        user: User,
        period: ReviewPeriod,
    ):
        self.user = user
        self.period = period

        self.state = ReviewSessionState.CREATED

        self.selected_fact = None

    def select_fact(self, fact: Fact):
        self.selected_fact = fact
        self.state = ReviewSessionState.CHOICE_DONE
