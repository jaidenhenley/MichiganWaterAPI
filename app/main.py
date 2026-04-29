import asyncio
from fastapi import FastAPI, HTTPException
from datetime import date

from app.data import beaches
from app.models import BeachModelResponse, Beach, NPSVisitation, BeachAlert

from dotenv import load_dotenv
load_dotenv()

from app.services.ndbc import fetch_ndbc_conditions
from app.services.nws import get_beach_alerts_safe
from app.services.water_quality import get_water_quality_safe
from app.services.holidays import is_holiday
from app.services.nps import fetch_nps_visitation, parse_nps_visitation, MICHIGAN_BEACH_PARKS

app = FastAPI()


@app.get("/nps/visitation/{park_code}", response_model=list[NPSVisitation])
async def get_nps_visitation(park_code: str, year: int = 2024):
    data = await fetch_nps_visitation(park_code=park_code.upper(), year=year)
    return parse_nps_visitation(data, park_code=park_code.upper())


@app.get("/nps/visitation", response_model=list[NPSVisitation])
async def get_all_nps_visitation(year: int = 2024):
    results = await asyncio.gather(
        *[fetch_nps_visitation(park_code=code, year=year) for code in MICHIGAN_BEACH_PARKS],
        return_exceptions=True,
    )
    all_entries = []
    for code, data in zip(MICHIGAN_BEACH_PARKS, results):
        if not isinstance(data, Exception):
            all_entries.extend(parse_nps_visitation(data, park_code=code))
    return all_entries


@app.get("/beaches/{beach_id}/details", response_model=BeachModelResponse)
async def get_beach(beach_id: int) -> BeachModelResponse:
    beach = next((b for b in beaches if b["id"] == beach_id), None)
    if not beach:
        raise HTTPException(status_code=404, detail="Beach not found")

    buoy_result, alerts_result = await asyncio.gather(
        fetch_ndbc_conditions(beach["buoyStation"]),
        get_beach_alerts_safe(beach["lake"]),
        return_exceptions=True,
    )

    buoy = buoy_result if not isinstance(buoy_result, Exception) else None
    alerts = alerts_result if not isinstance(alerts_result, Exception) else []



    water_quality = get_water_quality_safe(beach_id)

    return BeachModelResponse(
        beach=beach["name"],
        lake=beach["lake"],
        alerts=alerts,
        buoyData=buoy,
        holiday=is_holiday(date.today()),
        waterQuality=[water_quality] if water_quality is not None else []
    )
