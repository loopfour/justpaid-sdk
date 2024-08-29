# JustPaid API Python SDK

This SDK provides a simple interface to interact with the JustPaid API for usage-based billing.

## Installation

```bash
pip install justpaid
```

## Quick Start

```python
from justpaid import JustPaidAPI

# Initialize the API client
api = JustPaidAPI("https://api.justpaid.io", "your_api_token_here")

# Get billable items
items = api.get_billable_items()

print(items)
```

for more examples, see the [examples](examples/) directory.

## Features

- Retrieve billable items
- Ingest usage events
- Batch ingest multiple usage events


## Documentation

For detailed API documentation and examples, see the [docs](https://docs.justpaid.io/api-reference/) directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
