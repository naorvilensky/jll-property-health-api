import json
from functools import lru_cache
from typing import List, Dict, Any, Optional

from core.settings import get_settings


@lru_cache(maxsize=1)
def load_market_data() -> List[Dict[str, Any]]:
    settings = get_settings()
    with open(settings.MARKET_FILE, "r") as f:
        return json.load(f)


@lru_cache(maxsize=5)
def find_market(market_id: int) -> Optional[Dict[str, Any]]:
    for m in load_market_data():
        if m["market_id"] == market_id:
            return m
    return None
