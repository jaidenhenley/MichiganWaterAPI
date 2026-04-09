from app.models import Beach
from pydantic import BaseModel
from datetime import date

# Nearest NDBC buoy station IDs for reference
# 45007 = South Lake Michigan (seasonal — offline in winter)
# 45002 = North Lake Michigan
# 45008 = South Lake Huron
# 45005 = West Lake Erie
# 45006 = West Lake Superior (seasonal — offline in winter)
# 45024 = East Lake Michigan (near Grand Haven)
# 45214 = Lake Erie (near Detroit)

sample_beaches = [
    {
        "id": 1,
        "name": "Belle Isle Beach",
        "county": "Wayne",
        "latitude": 42.3416,
        "longitude": -82.9625,
        "lake": "Lake Erie",
        "buoyStation": "45214",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year

    },
    {
        "id": 2,
        "name": "Grand Haven State Park",
        "county": "Ottawa",
        "latitude": 43.0564,
        "longitude": -86.2545,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Advisory",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 3,
        "name": "Silver Lake Beach",
        "county": "Oceana",
        "latitude": 43.6753,
        "longitude": -86.5214,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
        
    },
    {
        "id": 4,
        "name": "Sleeping Bear Dunes",
        "county": "Leelanau",
        "latitude": 44.8779,
        "longitude": -86.0590,
        "lake": "Lake Michigan",
        "buoyStation": "45002",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
        
    },
    {
        "id": 5,
        "name": "Tawas Point State Park",
        "county": "Iosco",
        "latitude": 44.2572,
        "longitude": -83.4467,
        "lake": "Lake Huron",
        "buoyStation": "45008",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 6,
        "name": "Holland State Park",
        "county": "Ottawa",
        "latitude": 42.7789,
        "longitude": -86.2048,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 7,
        "name": "Ludington State Park",
        "county": "Mason",
        "latitude": 44.0349,
        "longitude": -86.5018,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 8,
        "name": "P.J. Hoffmaster State Park",
        "county": "Muskegon",
        "latitude": 43.1329,
        "longitude": -86.2654,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 9,
        "name": "Warren Dunes State Park",
        "county": "Berrien",
        "latitude": 41.9153,
        "longitude": -86.5934,
        "lake": "Lake Michigan",
        "buoyStation": "45007",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 10,
        "name": "Petoskey State Park",
        "county": "Emmet",
        "latitude": 45.4068,
        "longitude": -84.9086,
        "lake": "Lake Michigan",
        "buoyStation": "45002",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 11,
        "name": "Pictured Rocks National Lakeshore",
        "county": "Alger",
        "latitude": 46.5643,
        "longitude": -86.3163,
        "lake": "Lake Superior",
        "buoyStation": "45006",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 12,
        "name": "Presque Isle Park",
        "county": "Marquette",
        "latitude": 46.5880,
        "longitude": -87.3818,
        "lake": "Lake Superior",
        "buoyStation": "45006",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 13,
        "name": "Harrisville State Park",
        "county": "Alcona",
        "latitude": 44.6475,
        "longitude": -83.2976,
        "lake": "Lake Huron",
        "buoyStation": "45008",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 14,
        "name": "Sterling State Park",
        "county": "Monroe",
        "latitude": 41.9200,
        "longitude": -83.3415,
        "lake": "Lake Erie",
        "buoyStation": "45214",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 15,
        "name": "Muskegon State Park",
        "county": "Muskegon",
        "latitude": 43.2485,
        "longitude": -86.3339,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 16,
        "name": "Saugatuck Dunes State Park",
        "county": "Allegan",
        "latitude": 42.6968,
        "longitude": -86.1903,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 17,
        "name": "South Haven South Beach",
        "county": "Van Buren",
        "latitude": 42.4031,
        "longitude": -86.2736,
        "lake": "Lake Michigan",
        "buoyStation": "45024",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 18,
        "name": "Port Crescent State Park",
        "county": "Huron",
        "latitude": 44.0103,
        "longitude": -83.0508,
        "lake": "Lake Huron",
        "buoyStation": "45008",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 19,
        "name": "Albert E. Sleeper State Park",
        "county": "Huron",
        "latitude": 43.9726,
        "longitude": -83.2055,
        "lake": "Lake Huron",
        "buoyStation": "45008",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 20,
        "name": "McLain State Park",
        "county": "Houghton",
        "latitude": 47.2371,
        "longitude": -88.6088,
        "lake": "Lake Superior",
        "buoyStation": "45006",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
    {
        "id": 21,
        "name": "Porcupine Mountains Wilderness State Park",
        "county": "Ontonagon",
        "latitude": 46.7811,
        "longitude": -89.6807,
        "lake": "Lake Superior",
        "buoyStation": "45006",
        "status": "Safe",
        "countryCode": "US",
        "year": date.today().year
    },
]
