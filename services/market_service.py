import json
from functools import lru_cache
from typing import Dict, Any, List

from core.settings import get_settings

settings = get_settings()

@lru_cache(maxsize=1)
def load_property_data() -> List[Dict[str, Any]]:
    with open(settings.PROPERTY_FILE, "r") as f:
        return json.load(f)

@lru_cache(maxsize=1)
def load_market_data() -> List[Dict[str, Any]]:
    with open(settings.MARKET_FILE, "r") as f:
        return json.load(f)
