import json
from functools import lru_cache
from typing import List, Dict, Any, Optional

from core.settings import get_settings


@lru_cache(maxsize=1)
def load_property_data() -> List[Dict[str, Any]]:
    settings = get_settings()
    with open(settings.PROPERTY_FILE, "r") as f:
        return json.load(f)


@lru_cache(maxsize=100)
def find_property(property_id: int) -> Optional[Dict[str, Any]]:
    for p in load_property_data():
        if p["id"] == property_id:
            return p
    return None
