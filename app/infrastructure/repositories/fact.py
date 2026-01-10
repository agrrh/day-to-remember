import copy
from typing import List
from uuid import UUID

from app.domain.fact import Fact
from app.domain.review_period import ReviewPeriod, ReviewPeriodScope
from app.domain.review_session import ReviewSession
from app.domain.user import User
from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.utils.errors import BaseError


class ErrorFactRepository(BaseError):
    """Fact repository error."""


class ErrorFactNotFound(BaseError):
    """Fact not found."""


class ErrorMultipleFactsFound(BaseError):
    """Many Facts has same UUID?."""


class FactRepository:
    """Interface for Facts storage."""

    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Facts"

    def save(self, fact: Fact) -> bool:
        """Save Fact to database."""

        self.adapter.create_record(fact.model_dump())
        return True

    def get_by_uuid(self, uuid: str) -> Fact:
        """Get Fact by its UUID."""

        uuid = str(UUID(uuid))

        facts_found = self.adapter.get_records(
            filters={
                "uuid": uuid,
            }
        )

        match len(facts_found):
            case 0:
                raise ErrorFactNotFound
            case 1:
                _f = facts_found[0]
                fact = Fact(**_f)
            case _:
                raise ErrorMultipleFactsFound

        return fact

    def get_by_period(self, user: User, period: ReviewPeriod) -> List[Fact]:
        """Obtain Facts for User by specified Period."""

        if period.start is None or period.end is None:
            raise ErrorFactRepository

        query = """
            SELECT *
            FROM {table_id}
            WHERE
                user_uuid = '{user_uuid}'
                AND date BETWEEN unixepoch('{date_start}') AND unixepoch('{date_end}')
            ORDER BY date DESC
            LIMIT 100
        """.format(
            table_id=self.adapter.table_id,
            user_uuid=user.uuid,
            date_start=period.start.strftime("%Y-%m-%d"),
            date_end=period.end.strftime("%Y-%m-%d"),
        )
        data = self.adapter.get_records_sql(query=query)

        if not isinstance(data, dict) or "records" not in data:
            raise ErrorFactRepository

        facts_list = [
            Fact(**record.get("fields", {})) for record in data.get("records", [])
        ]

        return facts_list

    def get_by_review_session(self, user: User, rs: ReviewSession) -> List[Fact]:
        """Obtain Facts for User by specified ReviewSession."""

        if rs.period.start is None or rs.period.end is None:
            raise ErrorFactRepository

        match rs.period.scope:
            case ReviewPeriodScope.WEEK:
                scope_query = "= ''"

            case _:
                scope_query = "= 'z'"

        query = """
            SELECT *
            FROM {table_id}
            WHERE
                user_uuid = '{user_uuid}'
                AND date >= unixepoch('{date_start}') AND date <= unixepoch('{date_end}')
                AND reviewed_at_scope {scope_query}
            ORDER BY date DESC
            LIMIT 100
        """.format(
            table_id=self.adapter.table_id,
            user_uuid=user.uuid,
            scope_query=scope_query,
            date_start=rs.period.start.strftime("%Y-%m-%d"),
            date_end=rs.period.end.strftime("%Y-%m-%d"),
        )
        data = self.adapter.get_records_sql(query=query)

        if not isinstance(data, dict) or "records" not in data:
            raise ErrorFactRepository

        facts_list = [
            Fact(**record.get("fields", {})) for record in data.get("records", [])
        ]

        return facts_list

    def set_selected_for_scope(self, fact: Fact, scope: ReviewPeriodScope) -> bool:
        """Set selected_at_scope field to appropriate value."""
        fact.selected_at_scope = scope

        result = self.adapter.upsert_record(
            {
                "uuid": fact.uuid,
            },
            fact.model_dump(),
        )

        return bool(result)
