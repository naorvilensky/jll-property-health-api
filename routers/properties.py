from typing import Optional, List

from fastapi import APIRouter, Query
from schemas.property_schema import MarketPerformanceResponse
from services.market_service import get_property_market_performance

router = APIRouter(tags=["Properties"])


@router.get(
    "/{property_id}/market-performance",
    response_model=MarketPerformanceResponse
)
def property_market_performance(
        property_id: int,
        metrics: Optional[List[str]] = Query(None),
        include_history: Optional[bool] = Query(False),
):
    result = get_property_market_performance(property_id, metrics, include_history)

    return result
