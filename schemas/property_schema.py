from pydantic import BaseModel
from typing import List, Optional

class MetricComparison(BaseModel):
    name: str
    property_value: Optional[float]
    market_value: Optional[float]
    difference: Optional[float]
    percent_difference: Optional[float]

class MarketPerformanceResponse(BaseModel):
    property_id: int
    property_name: str
    market_id: int
    market_name: str
    comparison_date: Optional[str]
    metrics: List[MetricComparison]
