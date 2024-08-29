from justpaid.api import JustPaidAPI
from justpaid.schemas import UsageEvent, UsageEventRequest
from justpaid.exceptions import JustPaidAPIException


from datetime import datetime, timezone
import uuid

# Initialize the API with your token
api = JustPaidAPI(api_token="YOUR_API_TOKEN")

try:
    # Get billable items
    billable_items_response = api.get_billable_items()
    print("Billable Items:")
    for customers in billable_items_response.customers:
        print(f"Customer: {customers.customer_id}")
        for item in customers.items:
            print(f"  - Item: {item.item_name} (ID: {item.item_id})")

    # Use the first item_id from the response
    if billable_items_response.customers[0].items:
        customer_id = billable_items_response.customers[0].customer_id
        item = billable_items_response.customers[0].items[0]
        item_id = item.item_id
        item_name = item.item_name

        # Create a usage event
        event = UsageEvent(
            customer_id=customer_id,
            event_name=item_name,
            timestamp=datetime.now(timezone.utc),
            idempotency_key=str(uuid.uuid4()),
            item_id=item_id,
            event_value=1,
            external_customer_id="ext-customer-123",
            properties={
                "endpoint": "/users",
                "method": "GET",
                "response_time_ms": 150
            }
        )

        # Create a request with the event
        request = UsageEventRequest(events=[event])

        # Ingest the usage event
        response = api.ingest_usage_events(request)
        print("\nIngestion Response:")
        print(f"{response.info.created_events} created, and duplicates: {response.info.duplicates}")
       

        if response.errors:
            print("\nErrors:")
            for error in response.errors:
                print(f"- Event with key {error.idempotency_key}: {error.error}")

        # Batch ingest multiple events
        batch_events = [
            UsageEvent(
                customer_id=customer_id,
                event_name="data_transfer",
                timestamp=datetime.now(timezone.utc),
                idempotency_key=str(uuid.uuid4()),
                item_id=item_id,
                event_value=5.2,
                external_customer_id="ext-customer-123",
                properties={"file_type": "image", "size_mb": 5.2}
            ),
            UsageEvent(
                customer_id=customer_id,
                event_name="api_call",
                timestamp=datetime.now(timezone.utc),
                idempotency_key=str(uuid.uuid4()),
                item_id=item_id,
                event_value=1,
                external_customer_id="ext-customer-456",
                properties={"endpoint": "/products", "method": "POST"}
            )
        ]
        

        # pass duplicate idempotency key to test error handling
        batch_events.append(UsageEvent(
            customer_id=customer_id,
            event_name="api_call",
            timestamp=datetime.now(timezone.utc),
            idempotency_key=batch_events[0].idempotency_key,
            item_id=item_id,
            event_value=1,
            external_customer_id="ext-customer-456",
            properties={"endpoint": "/products", "method": "POST"}
        ))

        batch_request = UsageEventRequest(events=batch_events)
        batch_response = api.ingest_usage_events(batch_request)
        print("\nBatch Ingestion Response:")
        print(f"{batch_response.info.created_events} created, and duplicates: {batch_response.info.duplicates}")
        
        if batch_response.errors:
            print("\nBatch Errors:")
            for error in batch_response.errors:
                print(f"- Event with key {error.idempotency_key}: {error.error}")

    else:
        print("No billable items found")

except JustPaidAPIException as e:
    print(f"An error occurred: {str(e)}")
