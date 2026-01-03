import datetime

from app.domain.errors import DomainError


class ErrorReviewPeriodStartAfterEnd(DomainError):
    """ReviewPeriod start date must be after end date."""


class ReviewPeriod:
    def __init__(
        self,
        start: datetime.date,
        end: datetime.date,
    ):
        self.start = start
        self.end = end

    def create(self):
        if not self.start >= self.end:
            raise ErrorReviewPeriodStartAfterEnd

        # TODO: Gather facts to review

        # self.add_event(SomeEvent(param=self.param))


class ReviewPeriodWeek(ReviewPeriod):
    def __init__(self, end: datetime.date):
        self.end = end
        self.start = self.end - datetime.timedelta(days=7)


class ReviewPeriodMonth(ReviewPeriod):
    def __init__(self, end: datetime.date):
        self.end = end
        self.start = self.end - datetime.timedelta(days=28)

        # TODO: Month should be real month, calculate dates as "from 1 to 28/30/31 day"


# TODO: Implement Quarter with month-bound dates
# class ReviewPeriodQuarter(ReviewPeriod):
#     def __init__(self, end: datetime.date):
#         self.end = end
#         self.start = self.end - datetime.timedelta(days=90)

# TODO: Implement Year with proper dates 01-01 to 31-12
# class ReviewPeriodYear(ReviewPeriod):
#     def __init__(self, end: datetime.date):
#         self.end = end
#         self.start = self.end - datetime.timedelta(days=365)
