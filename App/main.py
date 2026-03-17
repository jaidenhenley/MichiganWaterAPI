from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.data import sample_beaches
from app.models import Beach

from app.services.ndbc import fetch_ndbc_conditions

app = FastAPI()


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


@app.get("/beaches/{beach_id}", response_model=Beach)
def get_beach(beach_id: int):
    for beach in sample_beaches:
        if beach["id"] == beach_id:
            return beach
    raise HTTPException(status_code=404, detail="Beach not found")