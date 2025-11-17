from functools import lru_cache
from typing import Dict, Any
from db.market_db import find_market
from db.property_db import find_property
import consts.scoring as scoring


def score_band(relative_diff: float) -> float:
    if relative_diff >= 0.10:
        return 95
    if relative_diff >= 0.05:
        return 85
    if relative_diff >= 0.00:
        return 70
    if relative_diff >= -0.05:
        return 55
    if relative_diff >= -0.10:
        return 35
    return 10


def score_single_kpi(prop_val: float, market_val: float, kpi_name: str) -> tuple[
    float | None, float | None, float | None]:
    if prop_val is None or market_val is None:
        return None, None, None

    if scoring.INVERTED_KPIS.get(kpi_name, False):
        relative = (market_val - prop_val) / market_val  # lower is better
    else:
        relative = (prop_val - market_val) / market_val  # higher is better

    score = score_band(relative)
    diff = prop_val - market_val
    pct = (diff / market_val) * 100
    return score, diff, pct


def score_all_kpis(property_data, latest_market, metric_pairs):
    metrics = []
    kpi_scores = {}

    for prop_key, market_key in metric_pairs:
        prop_val = property_data.get(prop_key)
        market_val = latest_market.get(market_key)

        score, diff, pct = score_single_kpi(prop_val, market_val, prop_key)
        kpi_scores[prop_key] = score

        metrics.append({
            "name": prop_key,
            "property_value": prop_val,
            "market_value": market_val,
            "difference": diff,
            "percent_difference": pct
        })

    return metrics, kpi_scores


def compute_category_scores(kpi_scores: dict) -> dict:
    category_scores = {}

    for category, kpis in scoring.KPI_WEIGHTS.items():
        total = 0.0
        for kpi, weight in kpis.items():
            if kpi_scores.get(kpi) is not None:
                total += kpi_scores[kpi] * weight
        category_scores[category] = total

    return category_scores


def compute_current_performance(category_scores: dict) -> float:
    return sum(
        category_scores[cat] * scoring.CATEGORY_WEIGHTS[cat]
        for cat in scoring.CATEGORY_WEIGHTS
    )


def compute_trend_score(performance_history, metric_pairs):
    if len(performance_history) < 3:
        return 50

    m_first = performance_history[-3]
    m_last = performance_history[-1]
    trend_scores = []

    for _, mk in metric_pairs:
        v0 = m_first.get(mk)
        v1 = m_last.get(mk)
        if v0 and v1:
            market_change = (v1 - v0) / v0
            trend_scores.append(score_band(-market_change))

    return sum(trend_scores) / len(trend_scores) if trend_scores else 50


def compute_data_quality(market_data):
    dq = market_data.get("data_quality_score", 0.8)
    conf = market_data.get("confidence_level", "medium")
    multiplier = scoring.CONFIDENCE_MULTIPLIER.get(conf, 0.8)
    return dq * multiplier * 100


def compute_final_health_score(current, trend, quality):
    score = (
            current * scoring.FINAL_WEIGHTS["current_performance"] +
            trend * scoring.FINAL_WEIGHTS["trend"] +
            quality * scoring.FINAL_WEIGHTS["data_quality"]
    )
    return max(0.0, min(100.0, score))


def compare_property_to_market(property_data, market_data):
    latest_market = market_data["performance"][-1]
    comparison_date = latest_market["date"]



    metrics, kpi_scores = score_all_kpis(property_data, latest_market, scoring.METRIC_PAIRS)
    category_scores = compute_category_scores(kpi_scores)
    current_performance = compute_current_performance(category_scores)
    trend_score = compute_trend_score(market_data["performance"], scoring.METRIC_PAIRS)
    data_quality_component = compute_data_quality(market_data)
    health_score = compute_final_health_score(current_performance, trend_score, data_quality_component)

    return {
        "property_id": property_data["id"],
        "property_name": property_data["name"],
        "market_id": market_data["market_id"],
        "market_name": market_data["market_name"],
        "comparison_date": comparison_date,
        "metrics": metrics,
        "health_score": round(health_score, 2),
        "health_components": {
            "current_performance": round(current_performance, 2),
            "trend": round(trend_score, 2),
            "data_quality": round(data_quality_component, 2),
        }
    }


@lru_cache(maxsize=10)
def get_property_market_performance(property_id: int):
    property_data = find_property(property_id)
    if not property_data:
        raise ValueError(f"Property {property_id} not found")

    market_data = find_market(property_data["market_id"])
    if not market_data:
        raise ValueError(f"Market {property_data['market_id']} not found")

    return compare_property_to_market(property_data, market_data)
