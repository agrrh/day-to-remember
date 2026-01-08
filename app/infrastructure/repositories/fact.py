import copy
from typing import List

from app.domain.fact import Fact
from app.domain.review_period import ReviewPeriod
from app.domain.user import User
from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.utils.errors import BaseError


class ErrorFactRepository(BaseError):
    """Fact repository error."""


class FactRepository:
    """Interface for Facts storage."""

    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Facts"

    def save(self, fact: Fact) -> bool:
        """Save Fact to database."""

        self.adapter.create_record(fact.model_dump())
        return True

    def get_by_period(self, user: User, period: ReviewPeriod) -> List[Fact]:
        """Obtain Facts for User by specified Period."""

        if period.start is None:
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
            Fact(**(record.get("fields", {}))) for record in data.get("records", [])
        ]

        return facts_list
