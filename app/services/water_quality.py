import requests
import zipfile
import io
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

from app.models import WaterQuality

_MAPPING_PATH = Path(__file__).parent.parent / "data" / "beach_station_map.json"
with open(_MAPPING_PATH) as f:
    BEACH_TO_STATION: dict[int, str] = {int(k): v for k, v in json.load(f).items()}

_cache: dict = {"df": None, "fetched_at": None}
_CACHE_TTL_HOURS = 24


def _fetch_recent_ecoli(days_back: int = 365) -> pd.DataFrame:
    end = datetime.now().strftime("%m-%d-%Y")
    start = (datetime.now() - timedelta(days=days_back)).strftime("%m-%d-%Y")
    
    url = (
        "https://www.waterqualitydata.us/data/Result/search"
        f"?statecode=US:26"
        f"&characteristicName=Escherichia%20coli"
        f"&startDateLo={start}"
        f"&startDateHi={end}"
        f"&mimeType=csv"
        f"&zip=yes"
    )
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f, low_memory=False)
    
    keep = [
        "ActivityStartDate",
        "MonitoringLocationIdentifier",
        "ResultMeasureValue",
        "ResultMeasure/MeasureUnitCode",
    ]
    return df[[c for c in keep if c in df.columns]]


def _get_results() -> pd.DataFrame:
    now = datetime.now()
    if (_cache["df"] is None or 
        _cache["fetched_at"] is None or 
        (now - _cache["fetched_at"]).total_seconds() > _CACHE_TTL_HOURS * 3600):
        _cache["df"] = _fetch_recent_ecoli()
        _cache["fetched_at"] = now
    return _cache["df"]


def get_water_quality(beach_id: int) -> Optional[WaterQuality]:
    station_id = BEACH_TO_STATION.get(beach_id)
    if station_id is None:
        return None
    
    df = _get_results()
    matches = df[df["MonitoringLocationIdentifier"] == station_id].copy()
    if matches.empty:
        return None
    
    matches["ActivityStartDate"] = pd.to_datetime(matches["ActivityStartDate"])
    latest = matches.sort_values("ActivityStartDate", ascending=False).iloc[0]
    
    value = latest["ResultMeasureValue"]
    if pd.isna(value):
        return None
    try:
        value = float(value)
    except (ValueError, TypeError):
        return None
    
    if value < 235:
        status = "safe"
    elif value < 300:
        status = "caution"
    else:
        status = "unsafe"
    
    return WaterQuality(
        lastReading=latest["ActivityStartDate"].strftime("%Y-%m-%d"),
        value=round(value, 1),
        unit=str(latest.get("ResultMeasure/MeasureUnitCode") or "MPN/100mL"),
        status=status,
        source="EGLE BeachGuard via EPA Water Quality Portal",
    )


def get_water_quality_safe(beach_id: int) -> Optional[WaterQuality]:
    """Wraps get_water_quality with error handling for use in routes."""
    try:
        return get_water_quality(beach_id)
    except Exception as e:
        print(f"[WaterQuality] Error for beach {beach_id}: {e}")
        return None