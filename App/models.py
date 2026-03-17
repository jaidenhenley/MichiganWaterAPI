from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    SAFE = "Safe"
    ADVISORY = "Advisory"
    CLOSED = "Closed"


class HazardLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    EXTREME = "Extreme"


class Beach(BaseModel):
    id: int
    name: str
    county: str
    status: Status
    ecoli_value: float
    latitude: float
    longitude: float
    lake: str
    buoy_station: str
    hazard_score: int


class WaterConditions(BaseModel):
    source: str = "NDBC"
    station_id: Optional[str] = None
    water_temp_c: Optional[float] = None
    wave_height_ft: Optional[float] = None
    wave_period_sec: Optional[float] = None
    wind_speed_mph: Optional[float] = None
    wind_direction: Optional[str] = None
    timestamp: Optional[datetime] = None


class WeatherAlert(BaseModel):
    headline: str
    severity: Optional[str] = None
    description: Optional[str] = None
    expires: Optional[datetime] = None


class HazardReport(BaseModel):
    beach_id: int
    beach_name: str
    hazard_score: int
    hazard_level: HazardLevel
    water_conditions: Optional[WaterConditions] = None
    weather_alerts: list[WeatherAlert] = Field(default_factory=list)
    ecoli_value: float
    summary: str