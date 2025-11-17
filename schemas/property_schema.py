from pydantic import BaseModel
from typing import List, Optional


class MetricComparison(BaseModel):
    name: str
    property_value: Optional[float]
    market_value: Optional[float]
    difference: Optional[float]
    percent_difference: Optional[float]


class HealthComponents(BaseModel):
    current_performance: float
    trend: float
    data_quality: float


class HistoricComparisonEntry(BaseModel):
    date: str
    property_value: Optional[float]
    market_value: Optional[float]
    relative_difference: Optional[float]
    score: Optional[float]


class HistoricComparison(BaseModel):
    metric: str
    history: List[HistoricComparisonEntry]


class MarketPerformanceResponse(BaseModel):
    property_id: int
    property_name: str
    market_id: int
    market_name: str
    comparison_date: Optional[str]
    metrics: List[MetricComparison]
    health_score: float
    health_components: HealthComponents
    historic_comparison: Optional[List[HistoricComparison]] = None
