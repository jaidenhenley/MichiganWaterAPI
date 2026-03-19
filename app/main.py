import asyncio
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

from app.data import sample_beaches
from app.models import Beach



from app.services.ndbc import fetch_ndbc_conditions
from app.services.nws import fetch_nws_alerts
from app.services.nws import fetch_weather_conditions

app = FastAPI()

@app.get("/alerts")
async def get_alerts(lat: float, lon: float):
    return await fetch_nws_alerts(lat, lon)

@app.get("/forecast/{station_id}")
async def get_weather_conditions(station_id: str):
    return await fetch_weather_conditions(station_id)

@app.get("/ndbc/{station_id}")
async def get_ndbc_conditions(station_id: str):
    return await fetch_ndbc_conditions(station_id)

@app.get("/")
def root():
    return {"message": "Michigan Water API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/beaches", response_model=list[Beach])
def get_beaches(
    county: Optional[str] = Query(None, description="Filter by county name"),
    lake: Optional[str] = Query(None, description="Filter by lake name"),
    status: Optional[str] = Query(None, description="Filter by status: safe, advisory, closed")
): 
    results = sample_beaches
    if county:
        results = [b for b in results if b["county"].lower() == county.lower()]
    if lake:
        results = [b for b in results if lake.lower() in b["lake"].lower()]
    if status:
        results = [b for b in results if b["status"].lower() == status.lower()]
    return results


@app.get("/beaches/{beach_id}/details")
async def get_beach(beach_id: int):
    beach = next((b for b in sample_beaches if b["id"] == beach_id), None)
    if not beach: 
        raise HTTPException(status_code=404, detail="Beach not found")

    weather_result, buoy_result, alerts_result = await asyncio.gather(
        fetch_weather_conditions(beach["nws_station_id"]),
        fetch_ndbc_conditions(beach["buoy_station"]),
        fetch_nws_alerts(beach["latitude"], beach["longitude"]),
        return_exceptions=True,
    )

    # Type-check each result — exceptions become None
    weather = weather_result if not isinstance(weather_result, Exception) else None
    buoy = buoy_result if not isinstance(buoy_result, Exception) else None
    alerts = alerts_result if not isinstance(alerts_result, Exception) else None

    return {
        "beach": beach["name"],
        "weather": weather,
        "buoy": buoy,
        "alerts": alerts,
    }