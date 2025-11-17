"""
Weights for calculation of health score
"""

# Metric pairs for trend score calculation
METRIC_PAIRS = [
    ("current_avg_rent_per_sqft", "avg_rent_per_sqft"),
    ("current_occupancy_rate", "avg_occupancy_rate"),
    ("renewal_rate_ytd", "renewal_rate"),
    ("avg_lease_term_months", "avg_lease_term_months"),
    ("avg_time_to_lease_days", "avg_time_to_lease_days"),
]

# KPI weights inside categories
KPI_WEIGHTS = {
    "financial": {
        "current_avg_rent_per_sqft": 1.0,
    },
    "occupancy": {
        "current_occupancy_rate": 0.5,
        "avg_lease_term_months": 0.3,
        "avg_time_to_lease_days": 0.2,
    },
    "retention": {
        "renewal_rate_ytd": 1.0,
    }
}

# Category-level weights for current performance score
CATEGORY_WEIGHTS = {
    "financial": 0.4,
    "occupancy": 0.4,
    "retention": 0.2,
}

# KPIs where lower values are better (inverse scoring)
INVERTED_KPIS = {
    "avg_time_to_lease_days": True
}

# Confidence multiplier for each confidence level
CONFIDENCE_MULTIPLIER = {
    "high": 1.0,
    "medium": 0.8,
    "low": 0.6
}

# Final composite score component weights
FINAL_WEIGHTS = {
    "current_performance": 0.6,
    "trend": 0.3,
    "data_quality": 0.1
}