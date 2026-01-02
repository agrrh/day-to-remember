import copy

from app.domain.fact import Fact

from app.infrastructure.external.grist_adapter import GristAdapter


class FactRepository:
    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Facts"

    def save(self, fact: Fact) -> bool:
        self.adapter.create_record(fact.dict())

        return True
