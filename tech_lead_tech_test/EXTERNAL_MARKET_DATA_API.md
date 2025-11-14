## External Market Data API Specification

Your implementation should integrate with an external market data API. Design your service layer to interact with the following endpoints:

### Endpoint 1: Get Market Data

```
GET /external-api/v1/markets/{marketId}/data
```

**Query Parameters**:
- `metrics` (optional): Comma-separated list of specific metrics to retrieve (e.g., "avg_rent_per_sqft,avg_occupancy_rate")
- `start_date` (optional): Start date for historical data (ISO 8601 format: YYYY-MM-DD)
- `end_date` (optional): End date for historical data (ISO 8601 format: YYYY-MM-DD)

**Example Request**:
```
GET /external-api/v1/markets/1/data?metrics=avg_rent_per_sqft,avg_occupancy_rate&start_date=2025-01-01&end_date=2025-03-01
```

**Example Response**:
```json
{
  "market_id": 1,
  "market_name": "Chicago Loop Office",
  "city": "Chicago",
  "state": "Illinois",
  "market_type": "office",
  "sample_size": 87,
  "data_quality_score": 0.95,
  "confidence_level": "high",
  "last_updated": "2025-09-03T14:30:00Z",
  "performance": [
    {
      "date": "2025-01-01",
      "avg_rent_per_sqft": 32.50,
      "avg_occupancy_rate": 82.3
    },
    {
      "date": "2025-02-01",
      "avg_rent_per_sqft": 33.10,
      "avg_occupancy_rate": 83.1
    },
    {
      "date": "2025-03-01",
      "avg_rent_per_sqft": 34.25,
      "avg_occupancy_rate": 84.7
    }
  ]
}
```

### Endpoint 2: Get Available Metrics

```
GET /external-api/v1/markets/{marketId}/metrics
```

**Example Request**:
```
GET /external-api/v1/markets/1/metrics
```

**Example Response**:
```json
{
  "market_id": 1,
  "available_metrics": [
    {
      "name": "avg_rent_per_sqft",
      "display_name": "Average Rent per Square Foot",
      "unit": "USD",
      "description": "Average rental rate per square foot across all properties in the market"
    },
    {
      "name": "avg_occupancy_rate",
      "display_name": "Average Occupancy Rate",
      "unit": "percentage",
      "description": "Average occupancy rate across all properties in the market"
    },
    {
      "name": "renewal_rate",
      "display_name": "Renewal Rate",
      "unit": "percentage",
      "description": "Percentage of leases renewed upon expiration"
    }
  ]
}
```
