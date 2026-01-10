from grist_api import GristDocAPI

from app.infrastructure.external.grist_sql import GristSQLAPI


class GristAdapter:
    """Adapter to interact with Grist database."""

    def __init__(self, url: str, document_id: str, api_key: str):
        self._client = GristDocAPI(document_id, server=url, api_key=api_key)
        self._client_sql = GristSQLAPI(
            document_id=document_id, server_url=url, api_key=api_key
        )
        self.table_id = "Table 1"

    def get_records(self, filters: dict | None = None) -> list[dict]:
        """Get records with default filters (supports "column=x" syntax)."""
        if filters is None:
            filters = {}
        return [
            r._asdict()
            for r in self._client.fetch_table(self.table_id, filters=filters)
        ]

    def get_records_sql(self, query: str) -> list[dict]:
        """Get records with default filters (supports select SQL syntax).

        Ref: https://support.getgrist.com/api/#tag/sql
        """
        return self._client_sql.query(query)

    def create_records(self, data_list: list[dict]) -> list[int]:
        """Add number of records to table."""

        row_ids = self._client.add_records(self.table_id, data_list)
        return row_ids

    def create_record(self, data: dict) -> int:
        """Create single record."""

        return self.create_records([data])[0]

    def upsert_record(self, match: dict, data: dict) -> list[dict]:
        """Upsert record that match "match" argument with "data" fields.

        Ref: https://support.getgrist.com/api/#tag/records/operation/replaceRecords
        """
        return self._client_sql.upsert(self.table_id, match, data)
