import datetime
from typing import Any, override

from pydantic import BaseModel

from app.domain.errors import DomainError


class ErrorReviewPeriodStartAfterEnd(DomainError):
    """ReviewPeriod start date must be after end date."""


class ReviewPeriod(BaseModel):
    """Basic review period."""

    end: datetime.date

    # May be calculated later
    start: datetime.date | None = None

    length: datetime.timedelta = datetime.timedelta(days=7)

    @override
    def model_post_init(self, context: Any) -> None:
        if self.start is not None and self.start >= self.end:
            raise ErrorReviewPeriodStartAfterEnd

        self.start = self.end - self.length


class ReviewPeriodWeek(ReviewPeriod):
    """One week."""

    length: datetime.timedelta = datetime.timedelta(days=7)


class ReviewPeriodMonth(ReviewPeriod):
    """One month."""

    # TODO: Month should be real month, calculate dates as "from 1 to 28/30/31 day"

    length: datetime.timedelta = datetime.timedelta(days=28)


# TODO: Implement Quarter with month-bound dates
# class ReviewPeriodQuarter(ReviewPeriod):
#     length: datetime.timedelta = datetime.timedelta(days=90)

# TODO: Implement Year with proper dates 01-01 to 31-12
# class ReviewPeriodYear(ReviewPeriod):
#     length: datetime.timedelta = datetime.timedelta(days=365)
