from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
from datetime import date
from typing import List


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
    latitude: float
    longitude: float
    lake: str
    buoyStation: str

class WaterConditions(BaseModel):
    source: str = "NDBC"
    station_id: Optional[str] = None
    water_temp_c: Optional[float] = None
    wave_height_m: Optional[float] = None
    wave_period_sec: Optional[float] = None
    wind_speed_mph: Optional[float] = None
    wind_direction: Optional[str] = None
    timestamp: Optional[datetime] = None


class Traffic(BaseModel):
    currentSpeed: int
    freeFlowSpeed: int
    currentTravelTime: int
    freeFlowTravelTime: int
    confidence: float
    roadClosures: bool
    
    
class NPSVisitation(BaseModel):
    park_code: str
    park_name: str
    year: int
    month: int
    recreation_visitors: int
    crowd_weight: float  # 0.0–1.0, normalized against peak month

class WaterQuality(BaseModel):
    lastReading: str
    value: float
    unit: str
    status: str
    source: str

class BeachModelResponse(BaseModel):
    beach: str
    buoyData: Optional[WaterConditions] = None
    alerts: List = []
    traffic: List[Traffic] = []
    holiday: bool = False
    waterQuality: Optional[WaterQuality] = None
