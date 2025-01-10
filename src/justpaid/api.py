from typing import Optional

import requests

from .exceptions import JustPaidAPIException
from .schemas import (
    BillableItemCustomer,
    BillableItemsResponse,
    Invoice,
    InvoiceListResponse,
    UsageDataBatchJobStatusResponse,
    UsageEventAsyncResponse,
    UsageEventRequest,
    UsageEventResponse,
)


class JustPaidAPI:
    BASE_URL = "https://api.justpaid.io/api/v1"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_billable_items(
        self,
        customer_id: Optional[str] = None,
        external_customer_id: Optional[str] = None,
    ) -> BillableItemsResponse:
        url = f"{self.BASE_URL}/usage/items"
        params = {}
        if customer_id:
            params["customer_id"] = customer_id
        if external_customer_id:
            params["external_customer_id"] = external_customer_id

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise JustPaidAPIException(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        try:
            customers = [BillableItemCustomer(**item) for item in response.json()]
        except KeyError as e:
            raise JustPaidAPIException(f"Missing expected field in response: {e}")

        return BillableItemsResponse(customers=customers)

    def ingest_usage_events(self, payload: UsageEventRequest) -> UsageEventResponse:
        url = f"{self.BASE_URL}/usage/ingest"

        response = requests.post(url, headers=self.headers, json=payload.dict())

        if response.status_code != 200:
            raise JustPaidAPIException(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        return UsageEventResponse(**response.json())

    def ingest_usage_events_async(
        self, payload: UsageEventRequest
    ) -> UsageEventResponse:
        url = f"{self.BASE_URL}/usage/ingest-async"

        response = requests.post(url, headers=self.headers, json=payload.dict())

        if response.status_code != 200:
            raise JustPaidAPIException(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        return UsageEventAsyncResponse(**response.json())

    def get_usage_data_batch_job_status(
        self, job_id: str
    ) -> UsageDataBatchJobStatusResponse:
        url = f"{self.BASE_URL}/usage/job_status/{job_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise JustPaidAPIException(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        return UsageDataBatchJobStatusResponse(**response.json())

        
        