import copy

from app.domain.fact import Fact
from app.infrastructure.external.grist_adapter import GristAdapter


class FactRepository:
    """Interface for Facts storage."""

    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Facts"

    def save(self, fact: Fact) -> bool:
        """Save Fact to database."""

        self.adapter.create_record(fact.model_dump())
        return True
