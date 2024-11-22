from justpaid.api import JustPaidAPI
from justpaid.schemas import UsageEvent, UsageEventRequest
from justpaid.exceptions import JustPaidAPIException


from datetime import datetime, timezone
import uuid

# Initialize the API with your token
api = JustPaidAPI(api_token="YOUR_API_TOKEN")

def get_billable_items_by_external_customer_id(external_customer_id: str):
    try:
        # Get billable items by external customer ID
        billable_items_response = api.get_billable_items(external_customer_id=external_customer_id)
        print("Billable Items:")
        print(billable_items_response.customers[0])

        return billable_items_response.customers[0]
    except JustPaidAPIException as e:
        print(f"An error occurred: {str(e)}")


def ingest_usage_event(customer_id: str,):
    try:
        usage_event = UsageEvent(
            customer_id=customer_id,
            event_name="ocr-api",
            quantity=10,
            idempotency_key=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
        )
        usage_event_request = UsageEventRequest(
            events=[usage_event]
        )
        api.ingest_usage_event(usage_event_request)
    except JustPaidAPIException as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Get billable items by external customer ID
    customer = get_billable_items_by_external_customer_id(external_customer_id="your-external-customer-id")

    # Ingest usage event
    ingest_usage_event(customer_id=customer.id)
          

