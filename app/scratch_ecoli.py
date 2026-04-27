import requests
import zipfile
import io
import pandas as pd
import json
import math

with open("app/coastcast_beach.json") as f:
    COASTCAST_SAMPLE = json.load(f)

STREAM_KEYWORDS = [
    "drain", "creek", "river", "ditch", "outfall", "tributary",
    "downstream", "upstream", "trib", "brook", " us ", " ds ", "d/s", "u/s",
    "rnge", "rng", "mile road", "at townline", "at mound", " dr.", " dr ", "drain ", "near sawyer", "near mears",
"oceana ", "alger ", "pas",
]

def filter_out_stream_sites(stations: pd.DataFrame) -> pd.DataFrame:
    name_lower = stations["MonitoringLocationName"].fillna("").str.lower()
    is_stream = name_lower.apply(lambda name: any(kw in name for kw in STREAM_KEYWORDS))
    return stations[~is_stream]

def fetch_michigan_ecoli(start: str = "01-01-2026", end: str = "04-27-2025") -> pd.DataFrame:
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
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f, low_memory=False)
    
    keep = [
        "OrganizationIdentifier",
        "OrganizationFormalName",
        "ActivityStartDate",
        "MonitoringLocationIdentifier",
        "ResultMeasureValue",
        "ResultMeasure/MeasureUnitCode",
    ]
    return df[[c for c in keep if c in df.columns]]

def fetch_michigan_stations() -> pd.DataFrame:
    url = (
        "https://www.waterqualitydata.us/data/Station/search"
        "?statecode=US:26"
        "&characteristicName=Escherichia%20coli"
        "&mimeType=csv"
        "&zip=yes"
    )
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f, low_memory=False)
    
    keep = [
        "MonitoringLocationIdentifier",
        "MonitoringLocationName",
        "LatitudeMeasure",
        "LongitudeMeasure",
    ]

    return df[[c for c in keep if c in df.columns]]

def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def match_beaches_to_stations(beaches, stations: pd.DataFrame, max_miles: float = 1.0):
    matches = []
    for beach in beaches:
        nearest_id = None
        nearest_name = None
        nearest_dist = float("inf")
        for _, station in stations.iterrows():
            dist = haversine_miles(
                beach["lat"], beach["lon"],
                station["LatitudeMeasure"], station["LongitudeMeasure"]
            )
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_id = station["MonitoringLocationIdentifier"]
                nearest_name = station["MonitoringLocationName"]

        matches.append({
            "beach_id": beach["id"],
            "beach_name": beach["name"],
            "station_id": nearest_id if nearest_dist <= max_miles else None,
            "station_name": nearest_name if nearest_dist <= max_miles else None,
            "distance_miles": round(nearest_dist, 2),
            "matched": nearest_dist <= max_miles,
        })
    return matches

if __name__ == "__main__":
    df = fetch_michigan_ecoli(start="01-01-2026", end="04-27-2026")
    print(f"Rows: {len(df)}")
    if len(df) > 0:
        print(df.head(10))
        print("Date range:", df["ActivityStartDate"].min(), "to", df["ActivityStartDate"].max())
    else:
        print("No 2026 readings yet.")

# if __name__ == "__main__":
#     print(f"Loaded {len(COASTCAST_SAMPLE)} beaches from JSON")
    
#     stations = fetch_michigan_stations()
#     stations = filter_out_stream_sites(stations)
#     print(f"Stations after stream filter: {len(stations)}")

#     matches = match_beaches_to_stations(COASTCAST_SAMPLE, stations, max_miles=1.0)
#     matched_count = sum(1 for m in matches if m["matched"])
    
#     print(f"Matched {matched_count}/{len(matches)} beaches\n")

#     # Map BeachID to StationID
#     beach_to_station = {
#         m["beach_id"]: m["station_id"]
#         for m in matches if m["matched"]
#     }

#     import os
#     output_path = "app/data/beach_station_map.json"
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, "w") as f:
#         json.dump(beach_to_station, f, indent=2)

#     print(f"Wrote {len(beach_to_station)} mappings to {output_path}")