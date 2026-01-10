import copy
import time

from app.domain.fact import Fact
from app.domain.review_period import ReviewPeriod
from app.domain.review_session import ReviewSessionStatus, ReviewSessionStored
from app.domain.user import User
from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.utils.errors import BaseError


class ErrorReviewSessionRepository(BaseError):
    """ReviewSession repository error."""


# TODO: Expand this notation to other errors?
class Error_ReviewSession_NotFound(BaseError):
    """ReviewSession not found."""


class Error_ReviewSession_PeriodIsNotInitialized(BaseError):
    """Period is not properly initialized, probably missing dates."""


class ReviewSessionRepository:
    """Interface for ReviewSession storage."""

    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Review_sessions"

    def save(self, rs: ReviewSessionStored) -> bool:
        """Save ReviewSession to database."""

        result = self.adapter.create_record(rs.model_dump())

        return bool(result)

    def upsert(self, rss: ReviewSessionStored) -> list[dict]:
        """Upsert ReviewSession in database."""

        result = self.adapter.upsert_record(
            {
                "uuid": rss.uuid,
            },
            rss.model_dump(),
        )

        return result

    def get_by_user_and_period(
        self,
        user: User,
        period: ReviewPeriod,
    ) -> ReviewSessionStored:
        """Get ReviewSession by specified Period."""

        if period.start is None:
            raise Error_ReviewSession_PeriodIsNotInitialized

        filters = {
            "user_uuid": user.uuid,
            "period_scope": period.scope,
            "date_start": time.mktime(period.start.timetuple()),
        }

        found = self.adapter.get_records(filters=filters)

        match len(found):
            case 0:
                raise Error_ReviewSession_NotFound
            case 1:
                rs = found[0]
                rs_obj = ReviewSessionStored(**rs)
            case _:
                raise ErrorReviewSessionRepository  # TODO: Use specific error

        return rs_obj

    def promote_fact(self, rss: ReviewSessionStored, fact: Fact) -> bool:
        """Set Fact selected for this ReviewSession."""

        # FIXME:  RS -> RSS transformation happens again, maybe merge it with "use_cases/plan_review_sessions.py" part?

        rss.selected_fact_uuid = fact.uuid
        rss.status = ReviewSessionStatus.COMPLETED

        return bool(self.upsert(rss))
