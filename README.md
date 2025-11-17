# Property Market Performance API

This service calculates property performance relative to its market using static JSON inputs. It provides KPI comparisons, a composite health score, optional KPI filtering, and optional market-history comparisons.

## Project Structure

```
.
├── consts/                # Scoring constants, metric weights, category weights
├── core/                  # Environment settings and configuration
├── db/                    # Data access for property and market records
├── routers/               # FastAPI route definitions
├── schemas/               # Pydantic response models
├── services/              # Business logic and scoring engine
├── data/                  # Static JSON datasets
├── main.py                # FastAPI application entrypoint
└── requirements.txt
```

## Environment Configuration

The application loads configuration values (such as dataset paths) from a `.env` file using `pydantic-settings`.

An `env.template` file is provided as a starting point.  
To run the application locally, copy and rename it:

```
cp env.template .env
```

Then update any values if needed.

If the `.env` file is missing, the application will fall back to the default dataset paths defined in `core/settings.py`.

## Data Model Overview

The data directory contains two static JSON files:

- `property_data.json` – property-level records including current KPI values.
- `market_data.json` – market-level records including multi-month performance history.

The service loads these files once at startup using a cached settings object.

## Scoring Model

The health score is composed of three weighted components:

1. **Current Performance (60 percent)**  
   Based on normalized differences between property KPIs and the latest market KPIs.  
   Each KPI has a weight, and KPIs are grouped into categories with their own category weights.

2. **Market Trend (30 percent)**  
   Calculated from the slope of the market performance over the last three historical entries.  
   Property-level trend is not available in the dataset, so market trend serves as a fallback.

3. **Data Quality (10 percent)**  
   Uses `data_quality_score` and `confidence_level` from the market dataset.

All normalization uses direction-aware scoring, accounting for whether higher or lower values are preferable for a specific KPI.

## Historical Comparison Feature

If requested via query parameter, the API returns a history of how the property's current KPI values compare to each month in the market's performance history.  
This produces a timeline of relative differences and their corresponding normalized scores.

This does not affect the health score; it is strictly an informational extension.

## API Endpoint

### GET `/api/properties/{id}/market-performance`

Returns property-to-market comparison, composite health score, and optionally historical comparison.

### Query Parameters

- `metrics` (optional, comma-separated list)  
  Returns only the specified KPIs in the `metrics` field of the response.  
  Filtering does not affect the health score.

- `include_history` (optional, boolean, default false)  
  When true, includes full historical comparison for every KPI.

### Example Request

```
GET /api/properties/3/market-performance?metrics=current_avg_rent_per_sqft&include_history=true
```

### Example Response (abridged)

```
{
  "property_id": 3,
  "property_name": "...",
  "market_id": 1,
  "market_name": "...",
  "comparison_date": "2025-08-01",
  "metrics": [
    {
      "name": "current_avg_rent_per_sqft",
      "property_value": 42.8,
      "market_value": 39.7,
      "difference": 3.1,
      "percent_difference": 7.8
    }
  ],
  "health_score": 78.1,
  "health_components": {
    "current_performance": 75.3,
    "trend": 62.0,
    "data_quality": 90.0
  },
  "historic_comparison": [
    {
      "metric": "current_avg_rent_per_sqft",
      "history": [
        { "date": "2025-06-01", "property_value": 42.8, "market_value": 39.0, "relative_difference": 0.097, "score": 85 },
        { "date": "2025-07-01", "property_value": 42.8, "market_value": 39.4, "relative_difference": 0.086, "score": 85 }
      ]
    }
  ]
}
```

## Caching Strategy

- Full unfiltered results are cached using `lru_cache`.
- Filtered or historical responses bypass the cache.
- The settings file uses `lru_cache` to create a singleton configuration instance.
- Market and property datasets are loaded once and reused.

## Local Development

```
pip install -r requirements.txt
fastapi dev main.py
```

The `.env` file (or `env.template`) controls the dataset paths.


## Running with Docker


This project includes a Dockerfile and a docker-compose configuration that allow the API to run in a containerized environment.

```
docker-compose up -d
```

## Testing

Tests are not included, but the scoring engine is designed as pure functions, making it straightforward to test:

- KPI scoring  
- Category weighting  
- Trend scoring  
- Data quality scoring  
- Filtering behavior  
- Historical comparison

## Notes

This implementation follows clean separation of concerns, uses pure functions for the scoring pipeline, and demonstrates production-style API structure and caching strategy.
