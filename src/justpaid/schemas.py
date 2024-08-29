from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class UsageEvent(BaseModel):
    customer_id: Optional[str] = Field(None, description="The unique identifier for the customer. This can be either an email or a UUID obtained from JustPaid Platform.")
    event_name: str = Field(..., description="The name of the event being recorded, in snake_case format without spaces. For example: 'customer_created'.")
    timestamp: str = Field(..., description="The timestamp when the event occurred, in ISO 8601 format. The timestamp should be in UTC timezone.")
    idempotency_key: str = Field(..., description="A unique UUID key to ensure idempotency of event processing. This key is used to identify duplicate events.")
    item_id: Optional[str] = Field(None, description="An optional UUID that the event can be associated with. If provided, this should be a UUID obtained from JustPaid Platform using `api/v1/usage/events` endpoint.")
    event_value: float = Field(..., description="The value associated with the event. This can be either an integer or a float, this value is used to calculate the billing amount for the customer provided that a billing metric is associated with the event.")
    external_customer_id: Optional[str] = Field(None, description="An optional external identifier for the customer, provided as a string. This is used as an alias to JustPaid customer.")
    properties: Optional[Dict[str, Any]] = Field(None, description="An optional dictionary containing additional properties or metadata associated with the event.")

    @validator('timestamp', pre=True)
    def parse_timestamp(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class UsageEventRequest(BaseModel):
    events: List[UsageEvent]

class EventInfo(BaseModel):
    created_events: int
    duplicates: List[str]

class ErrorInfo(BaseModel):
    idempotency_key: str
    error: str

class UsageEventResponse(BaseModel):
    info: EventInfo = Field(..., description="Detailed information about the customer event ingestion process.")
    errors: Optional[List[ErrorInfo]] = Field(None, description="A list of errors that occurred during the ingestion process.")

class BillableItem(BaseModel):
    item_id: str = Field(..., description="The unique identifier for the item.")
    item_name: str = Field(..., description="The name of the item, typically describing what the billable item is about.")

class BillableItemCustomer(BaseModel):
    customer_id: str
    external_customer_id: Optional[str] = Field(None, description="An external identifier for the customer mapped by external systems.")
    customer_name: Optional[str] = Field(None, description="The name of the customer. This field is optional and can be used for display purposes.")
    customer_email: Optional[str] = Field(None, description="The email address of the customer. Optional and can be used for communication.")
    items: List[BillableItem]

class BillableItemsResponse(BaseModel):
    customers: List[BillableItemCustomer]
