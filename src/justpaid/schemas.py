from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, validator


class UsageEvent(BaseModel):
    customer_id: Optional[str] = Field(
        None,
        description="The unique identifier for the customer. This can be either an email or a UUID obtained from JustPaid Platform.",
    )
    event_name: str = Field(
        ...,
        description="The name of the event being recorded, in snake_case format without spaces. For example: 'customer_created'.",
    )
    timestamp: str = Field(
        ...,
        description="The timestamp when the event occurred, in ISO 8601 format. The timestamp should be in UTC timezone.",
    )
    idempotency_key: str = Field(
        ...,
        description="A unique UUID key to ensure idempotency of event processing. This key is used to identify duplicate events.",
    )
    item_id: Optional[str] = Field(
        None,
        description="An optional UUID that the event can be associated with. If provided, this should be a UUID obtained from JustPaid Platform using `api/v1/usage/events` endpoint.",
    )
    event_value: float = Field(
        ...,
        description="The value associated with the event. This can be either an integer or a float, this value is used to calculate the billing amount for the customer provided that a billing metric is associated with the event.",
    )
    external_customer_id: Optional[str] = Field(
        None,
        description="An optional external identifier for the customer, provided as a string. This is used as an alias to JustPaid customer.",
    )
    properties: Optional[dict[str, Any]] = Field(
        None,
        description="An optional dictionary containing additional properties or metadata associated with the event.",
    )

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class UsageEventRequest(BaseModel):
    events: list[UsageEvent]


class EventInfo(BaseModel):
    created_events: int
    duplicates: list[str]


class ErrorInfo(BaseModel):
    idempotency_key: str
    error: str


class UsageEventResponse(BaseModel):
    info: EventInfo = Field(
        ...,
        description="Detailed information about the customer event ingestion process.",
    )
    errors: Optional[list[ErrorInfo]] = Field(
        None, description="A list of errors that occurred during the ingestion process."
    )


class BillableItem(BaseModel):
    item_id: str = Field(..., description="The unique identifier for the item.")
    item_name: str = Field(
        ...,
        description="The name of the item, typically describing what the billable item is about.",
    )
    billing_alias: Optional[str] = Field(
        None,
        description="The billing alias for the item, this is the name that will be used to calculate the billing amount for the customer.",
    )


class BillableItemCustomer(BaseModel):
    customer_id: str
    external_customer_id: Optional[str] = Field(
        None,
        description="An external identifier for the customer mapped by external systems.",
    )
    customer_name: Optional[str] = Field(
        None,
        description="The name of the customer. This field is optional and can be used for display purposes.",
    )
    customer_email: Optional[str] = Field(
        None,
        description="The email address of the customer. Optional and can be used for communication.",
    )
    items: list[BillableItem]


class BillableItemsResponse(BaseModel):
    customers: list[BillableItemCustomer]


class UsageEventAsyncResponse(BaseModel):
    job_id: str = Field(..., description="The unique identifier for the job.")
    status: str = Field(..., description="The status of the job.")
    created_at: str = Field(..., description="The timestamp when the job was created.")
    total_events: int = Field(..., description="The total number of events in the job.")


class UsageDataBatchJobStatusResponse(BaseModel):
    job_id: str = Field(..., description="The unique identifier for the job.")
    status: str = Field(..., description="The status of the job.")
    created_at: str = Field(..., description="The timestamp when the job was created.")
    updated_at: str = Field(
        ..., description="The timestamp when the job was last updated."
    )
    info: Optional[EventInfo] = Field(
        None,
        description="Detailed information about the customer event ingestion process.",
    )
    errors: Optional[list[ErrorInfo]] = Field(
        None, description="A list of errors that occurred during the ingestion process."
    )
    total_events: int = Field(..., description="The total number of events in the job.")


class InvoiceCustomer(BaseModel):
    external_id: Optional[str] = Field(
        None,
        description="An optional external identifier for the customer. This can be used to link the customer to an external system.",
    )
    uuid: str = Field(..., description="The unique identifier for the customer")
    name: Optional[str] = Field(None, description="Customer name")
    contact_name: Optional[str] = Field(
        None, description="The name of the contact person"
    )
    email: Optional[str] = Field(None, description="Customer email")
    additional_emails: Optional[list[str]] = Field(
        None, description="A list of additional customer email addresses"
    )
    billing_emails: Optional[list[str]] = Field(
        None, description="Billing email addresses"
    )
    phone_number: Optional[str] = Field(
        None, description="Customer phone number with country code"
    )
    currency: Optional[str] = Field(None, description="Customer currency")
    tax_id: Optional[str] = Field(None, description="Customer tax id")


class InvoiceInvoiceLineItem(BaseModel):
    name: str = Field(..., description="The name of the line item")
    unit_price: float = Field(..., description="The price per unit for this line item")
    quantity: float = Field(..., description="The quantity of units for this line item")
    amount: float = Field(
        ..., description="The total amount for this line item (unit_price * quantity)"
    )
    currency: str = Field(..., description="The currency code for this line item")
    description: Optional[str] = Field(
        None, description="Additional details about the line item"
    )


class Invoice(BaseModel):
    uuid: str = Field(..., description="The unique identifier for the invoice")
    invoice_status: str = Field(..., description="The current status of the invoice")
    amount: float = Field(..., description="The total amount due for the invoice")
    currency: str = Field(..., description="The currency code for the invoice")
    invoice_number: str = Field(..., description="The unique invoice number")
    invoice_date: str = Field(..., description="The date when the invoice was created")
    due_date: Optional[str] = Field(
        None, description="The date by which the invoice must be paid"
    )
    service_start_date: Optional[str] = Field(
        None, description="The start date of the service period"
    )
    service_end_date: Optional[str] = Field(
        None, description="The end date of the service period"
    )
    description: Optional[str] = Field(None, description="A description of the invoice")
    created_at: str = Field(
        ..., description="The timestamp when the invoice was created"
    )
    is_recurring: bool = Field(
        ..., description="Indicates if this is a recurring invoice"
    )
    from_external_source: bool = Field(
        ..., description="Indicates if the invoice was created from an external source"
    )
    external_source: Optional[str] = Field(
        None, description="The name of the external source if applicable"
    )
    external_source_id: Optional[str] = Field(
        None, description="The ID of the invoice in the external system"
    )
    payment_link: Optional[str] = Field(
        None, description="URL where the customer can pay this invoice"
    )
    line_items: list[InvoiceInvoiceLineItem] = Field(
        ..., description="List of line items included in this invoice"
    )
    file_url: Optional[str] = Field(None, description="URL to download the invoice PDF")
    customer: Optional[InvoiceCustomer] = Field(
        None, description="Details of the customer associated with this invoice"
    )


class InvoiceListResponse(BaseModel):
    items: list[Invoice]
    count: int = Field(..., description="The total number of invoices")
