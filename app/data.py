from app.models import Beach
from pydantic import BaseModel

# Nearest NDBC buoy station IDs for reference
# 45007 = South Lake Michigan
# 45002 = North Lake Michigan
# 45008 = South Lake Huron
# 45005 = West Lake Erie
# 45006 = West Lake Superior

sample_beaches = [
    {
        "id": 1,
        "name": "Belle Isle Beach",
        "county": "Wayne",
        "latitude": 42.3416,
        "longitude": -82.9625,
        "lake": "Lake Erie",
        "buoy_station": "45147",
        "status": "Safe",
        "nws_station_id": "KDET"
    },
    {
        "id": 2,
        "name": "Grand Haven State Park",
        "county": "Ottawa",
        "latitude": 43.0564,
        "longitude": -86.2545,
        "lake": "Lake Michigan",
        "buoy_station": "45024",
        "status": "Advisory",
        "nws_station_id": "KMKG"
    },
    {
        "id": 3,
        "name": "Silver Lake Beach",
        "county": "Oceana",
        "latitude": 43.6753,
        "longitude": -86.5214,
        "lake": "Lake Michigan",
        "buoy_station": "45024",
        "status": "Safe",
        "nws_station_id": "KMKG"
    },
    {
        "id": 4,
        "name": "Sleeping Bear Dunes",
        "county": "Leelanau",
        "latitude": 44.8779,
        "longitude": -86.0590,
        "lake": "Lake Michigan",
        "buoy_station": "45002",
        "status": "Safe",
        "nws_station_id": "KTVC"
        
    },
    {
        "id": 5,
        "name": "Tawas Point State Park",
        "county": "Iosco",
        "latitude": 44.2572,
        "longitude": -83.4467,
        "lake": "Lake Huron",
        "buoy_station": "45008",
        "status": "Safe",
        "nws_station_id": "KOSC"
    },
]
