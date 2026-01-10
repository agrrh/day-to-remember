import calendar
import datetime
from enum import Enum
from typing import Any, override

from pydantic import BaseModel

from app.domain.errors import DomainError


class ErrorReviewPeriodStartAfterEnd(DomainError):
    """ReviewPeriod start date must be after end date."""


class ReviewPeriodScope(str, Enum):
    """Possible period scopes."""

    PRE_WEEK = "pre_week"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class ReviewPeriod(BaseModel):
    """Basic review period."""

    date: datetime.date
    scope: ReviewPeriodScope

    start: datetime.date | None = None  # Calculated later
    end: datetime.date | None = None  # Calculated later

    def adjust(self):
        """Each ReviewPeriod should have .adjust() method to allow instantiate proper periods for any given date in its boundaries.

        For base ReviewPeriod it does nothing.
        """
        pass

    @override
    def model_post_init(self, context: Any) -> None:
        self.adjust()


class ReviewPeriodWeek(ReviewPeriod):
    """One week."""

    scope: ReviewPeriodScope = ReviewPeriodScope.WEEK

    @override
    def adjust(self):
        start = self.date

        while start.isoweekday() > 1:
            start -= datetime.timedelta(days=1)

        self.start = start
        self.end = self.start + datetime.timedelta(days=6)


class ReviewPeriodMonth(ReviewPeriod):
    """One month."""

    scope: ReviewPeriodScope = ReviewPeriodScope.MONTH

    @override
    def adjust(self):
        start = self.date

        while int(start.strftime("%d")) > 1:
            start -= datetime.timedelta(days=1)

        _, days_in_month = calendar.monthrange(start.year, start.month)

        self.start = start
        self.end = self.start + datetime.timedelta(days=days_in_month - 1)


# TODO: Implement Quarter with month-bound dates
# TODO: Implement Year with proper dates 01-01 to 31-12
