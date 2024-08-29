import requests
from typing import Optional
from .schemas import (
    BillableItem, BillableItemCustomer, UsageEventRequest, 
    UsageEventResponse, BillableItemsResponse
)
from .exceptions import JustPaidAPIException

class JustPaidAPI:
    BASE_URL = "https://api.justpaid.io/api/v1"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def get_billable_items(self, customer_id: Optional[str] = None) -> BillableItemsResponse:
        url = f"{self.BASE_URL}/usage/items"
        params = {"customer_id": customer_id} if customer_id else {}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            raise JustPaidAPIException(f"API request failed with status {response.status_code}: {response.text}")
        
        try:
            customers = [BillableItemCustomer(**item) for item in response.json()]
        except KeyError as e:
            raise JustPaidAPIException(f"Missing expected field in response: {e}")
        
        return BillableItemsResponse(customers=customers)

    def ingest_usage_events(self, payload: UsageEventRequest ) -> UsageEventResponse:
        url = f"{self.BASE_URL}/usage/ingest"

        response = requests.post(url, headers=self.headers, json=payload.dict())
        
        if response.status_code != 200:
            raise JustPaidAPIException(f"API request failed with status {response.status_code}: {response.text}")
        
        return UsageEventResponse(**response.json())
