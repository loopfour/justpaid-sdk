import random
from justpaid.api import JustPaidAPI
from justpaid.schemas import UsageEvent, UsageEventRequest
from justpaid.exceptions import JustPaidAPIException

from datetime import datetime, timedelta, timezone
import time
import uuid
import sys
import itertools

# Initialize the API with your token
api = JustPaidAPI(api_token="YOUR_API_TOKEN")


def get_all_billable_items():
    try:
        billable_items_response = api.get_billable_items()
        print("Billable Items:")
        for customer in billable_items_response.customers:
            print(customer)
    except JustPaidAPIException as e:
        print(f"An error occurred: {str(e)}")

def get_billable_items_by_external_customer_id(external_customer_id: str):
    try:
        # Get billable items by external customer ID
        billable_items_response = api.get_billable_items(external_customer_id=external_customer_id)
        print("Billable Items:")
        print(billable_items_response.customers[0])

        return billable_items_response.customers[0]
    except JustPaidAPIException as e:
        print(f"An error occurred: {str(e)}")


def ingest_usage_events_async(usage_events):
    """
    Ingests usage events asynchronously and displays processing status.

    Args:
        usage_events (list): List of UsageEvent objects to be ingested.

    Returns:
        None
    """
    try:
        # Ingest usage events asynchronously
        usage_event_request = UsageEventRequest(events=usage_events)
        response = api.ingest_usage_events_async(usage_event_request)
        print("Usage events ingestion started...")

        # Start measuring processing time
        start_time = time.time()

        # Show a loading icon while polling job status
        spinner = itertools.cycle(['|', '/', '-', '\\'])

        # Poll the job status until it is complete
        job_status = api.get_usage_data_batch_job_status(response.job_id)
        while job_status.status not in ["SUCCESS", "FAILED"]:
            sys.stdout.write('\rProcessing ' + next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            job_status = api.get_usage_data_batch_job_status(response.job_id)

        # Calculate processing time
        end_time = time.time()
        processing_time = end_time - start_time

        # Clear the loading icon
        sys.stdout.write('\r')
        sys.stdout.flush()

        # Check final job status
        if job_status.status == "SUCCESS":
            print("Usage events ingestion completed successfully.")
            print(f"Processing time: {processing_time:.2f} seconds")
            print(f"Total events processed: {len(usage_events)}")
            print("Job details:")
            print(job_status)
        elif job_status.status == "FAILED":
            print("Usage events ingestion failed.")
            print("Error details:")
            print(job_status)

        # Provide a nice summary
        print("==============================")
        print("        Ingestion Summary      ")
        print("==============================")
        print(f"Status: {job_status.status}")
        print(f"Processing Time: {processing_time:.2f} seconds")
        print(f"Total Events Processed: {len(usage_events)}")

    except JustPaidAPIException as e:
        print(f"An error occurred during ingestion: {str(e)}")



if __name__ == "__main__":
    usage_events = []
    for i in range(3000):
        # Get a random timestamp in the last 30 days
        timestamp = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))
        usage_event = UsageEvent(
            customer_id="customer-id",
            event_name="event-name",
            idempotency_key=str(uuid.uuid4()),
            timestamp=timestamp,
            event_value=1,
            properties={
                "test": "test"
            }
        )
        usage_events.append(usage_event)

    # Call the separate method to ingest usage events asynchronously
    ingest_usage_events_async(usage_events)

          

