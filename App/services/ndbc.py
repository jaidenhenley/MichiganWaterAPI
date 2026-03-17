from typing import Optional
import httpx

from app.models import WaterConditions

def _parse_float(value: str) -> Optional[float]:
    if value == "MM":
        return None
    try: 
        return float(value)
    except ValueError: 
        return None
    

async def fetch_ndbc_conditions(station_id: str) -> WaterConditions:
    url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"

    headers = {
        "User-Agent": "MichiganWaterAPI/1.0 (learning project)"
    }

    async with httpx.AsyncClient(timeout=10.0, headers=headers) as Client: 
        response = await Client.get(url)
        response.raise_for_status()
    lines = response.text.strip().splitlines()
    if len(lines) < 3:
        raise ValueError(f"No usable NDBC data found for station {station_id}")
    # Line 0 = column names
    # Line 1 = Unit/Secondary Labels
    # Line 2 = First actual observation
    columns = lines[0].split()
    first_row = lines[2].split()
    if len(first_row) < len(columns):
        raise ValueError(f"Malformed NDBC row for station {station_id}")
    row = dict(zip(columns, first_row))

    return WaterConditions(
        station_id=station_id,
        water_temp_c=_parse_float(row.get("WTMP", "MM")),
        wave_height_m=_parse_float(row.get("WVHT", "MM"))
    )