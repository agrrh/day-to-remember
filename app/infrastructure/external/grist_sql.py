from typing import List

import requests

from app.infrastructure.utils.errors import BaseError


class ErrorGristSQLAPI(BaseError):
    """Could not get ANY response from Grist API SQL endpoint."""


class ErrorGristSQLAPIBadResponse(BaseError):
    """Could not get PROPER response from Grist API SQL endpoint."""


class GristSQLResponse:
    """Object Grist respond with."""

    statement: str
    records: List[dict]


class GristSQLAPI:
    """Simple adapter to send SQL requests to Grist API as those not supported in public module.

    Ref: https://github.com/gristlabs/py_grist_api/
    """

    # TODO: Merge request to GristAPI

    def __init__(self, server_url: str, api_key: str, document_id: str):
        self.server_url = server_url  # e.g. "https://test.example.org/grist"
        self.document_id = document_id
        self.api_key = api_key

        # TODO: Validate document_id as uuid?
        # https://support.getgrist.com/api/#tag/sql/paths/~1docs~1{docId}~1sql/post

    def __call(
        self,
        sql: str,
    ) -> GristSQLResponse:
        url = f"{self.server_url}/api/docs/{self.document_id}/sql"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "q": sql,
        }

        try:
            resp = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=60,
            )
        except Exception:
            raise ErrorGristSQLAPI

        if resp.status_code != 200:
            raise ErrorGristSQLAPIBadResponse

        return resp.json()

    def query(self, query: str):
        """Send a query."""
        # TODO: Add logging, error handling?
        return self.__call(query)
