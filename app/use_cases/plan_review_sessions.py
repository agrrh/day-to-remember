import datetime
import json
import time

from app.domain.review_period import ReviewPeriodScope, ReviewPeriodWeek
from app.domain.review_session import (
    ReviewSession,
    ReviewSessionStatus,
    ReviewSessionStored,
)
from app.infrastructure.env import DEV_RUN, DEV_USER_UUID_LIST
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.review_session import (
    Error_ReviewSession_NotFound,
    ReviewSessionRepository,
)
from app.infrastructure.repositories.user import UserRepository


class PlanReviewSessionsUseCase:
    """Form ReviewSessions for Users."""

    def __init__(
        self,
        user_repository: UserRepository,
        fact_repository: FactRepository,
        rs_repository: ReviewSessionRepository,
    ):
        self.fact_repository = fact_repository
        self.user_repository = user_repository
        self.rs_repository = rs_repository

    def __call__(self):
        """Entrypoint for this use case."""
        users = self.user_repository.get_active_users()

        today = datetime.date.today()

        if DEV_RUN:
            users = filter(lambda u: u.uuid in DEV_USER_UUID_LIST, users)

        for user in users:
            # WEEK

            # TODO: Also process other periods

            scope = ReviewPeriodScope.WEEK

            period = ReviewPeriodWeek(scope=scope, date=today)

            # Find ReviewSession by User and Period
            try:
                rs_stored = self.rs_repository.get_by_user_and_period(
                    user, period
                )

                selected_fact = None
                if rs_stored.selected_fact_uuid:
                    selected_fact = self.fact_repository.get_by_uuid(
                        rs_stored.selected_fact_uuid
                    )

                facts = []
                if isinstance(rs_stored.fact_uuids, list):
                    facts = [
                        self.fact_repository.get_by_uuid(fact_uuid)
                        for fact_uuid in rs_stored.fact_uuids
                    ]

                rs = ReviewSession(
                    uuid=rs_stored.uuid,
                    user=user,
                    period=period,
                    status=rs_stored.status,
                    facts=facts,
                    selected_fact=selected_fact,
                )
            except Error_ReviewSession_NotFound:
                rs = ReviewSession(user=user, period=period)

            # Collect/refresh Facts for current ReviewSession
            rs.facts = self.fact_repository.get_by_review_session(user, rs)
            rs.status = ReviewSessionStatus.COLLECTED

            # TODO: Get rid of this, we should not even convert date to unix timestamps here
            if not (
                hasattr(period.start, "timetuple")
                and hasattr(period.end, "timetuple")
            ):
                raise ValueError

            rs_stored = ReviewSessionStored(
                uuid=rs.uuid,
                user_uuid=rs.user.uuid,
                period_scope=rs.period.scope,
                date_start=time.mktime(period.start.timetuple()),
                date_end=time.mktime(period.end.timetuple()),
                fact_uuids=json.dumps(
                    [_.uuid for _ in rs.facts]
                ),  # ty: ignore[invalid-argument-type]
                status=rs.status,
            )

            self.rs_repository.upsert(rs_stored)
