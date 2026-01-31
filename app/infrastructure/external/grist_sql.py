from typing import Callable, List

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
        path: str,
        params: dict,
        body: dict,
        method: Callable = requests.get,
    ) -> GristSQLResponse:
        url = f"{self.server_url}/api/docs/{self.document_id}/{path}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            resp = method(
                url,
                headers=headers,
                params=params,
                json=body,
                timeout=60,
            )
        except Exception:
            raise ErrorGristSQLAPI

        if resp.status_code != 200:
            # TODO: Add debug-level logging of following values: url, params, body, resp.status_code, resp.text
            print("Error during Grist SQL request, debug info:", url, params, body)
            print("Grist response: ", resp.status_code, resp.text)
            raise ErrorGristSQLAPIBadResponse

        return resp.json()

    def __call_api(
        self, path: str, params: dict, body: dict, method: Callable = requests.get
    ):
        """Send a call to API."""
        return self.__call(method=method, path=path, params=params, body=body)

    def __call_sql(self, q: str):
        """Send an SQL call to API."""
        path = "sql"
        params = {
            "q": q,
        }
        body = {}
        return self.__call(path=path, params=params, body=body)

    def query(self, q: str):
        """Send a query."""
        # TODO: Add logging, error handling?
        return self.__call_sql(q)

    def upsert(self, table_id: str, match: dict, data: dict):
        """Update or add records."""

        params = {}
        body = {
            "records": [
                {
                    "require": match,
                    "fields": data,
                }
            ]
        }

        return self.__call_api(
            method=requests.put,
            path=f"tables/{table_id}/records",
            params=params,
            body=body,
        )
