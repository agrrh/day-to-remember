from grist_api import GristDocAPI


class GristAdapter:
    def __init__(self, url: str, document_id: str, api_key: str):
        self._client = GristDocAPI(document_id, server=url, api_key=api_key)
        self.table_id = "Table 1"

    def get_records(self, filters: dict = None) -> list[dict]:
        return self._client.fetch_table(self.table_id, filters=filters)

    def create_records(self, data_list: list[dict]) -> list[int]:
        row_ids = self._client.add_records(self.table_id, data_list)
        return row_ids

    def create_record(self, data: dict) -> int:
        return self.create_records([data])[0]
