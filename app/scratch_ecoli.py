import requests
import zipfile
import io
import pandas as pd
import json
import math
from datetime import datetime, timedelta

with open("app/coastcast_beach.json") as f:
    COASTCAST_SAMPLE = json.load(f)

STREAM_KEYWORDS = [
    "drain", "creek", "river", "ditch", "outfall", "tributary",
    "downstream", "upstream", "trib", "brook", " us ", " ds ", "d/s", "u/s",
    "rnge", "rng", "mile road", "at townline", "at mound", " dr.", " dr ",
    "drain ", "near sawyer", "near mears", "oceana ", "alger ", "pas",
]

CONTAMINANTS = [
    "Escherichia coli",
]


def filter_out_stream_sites(stations: pd.DataFrame) -> pd.DataFrame:
    name_lower = stations["MonitoringLocationName"].fillna("").str.lower()
    is_stream = name_lower.apply(lambda name: any(kw in name for kw in STREAM_KEYWORDS))
    return stations[~is_stream]


def fetch_michigan_contaminants(contaminants: list, days_back: int = 30) -> pd.DataFrame:
    end = datetime.now().strftime("%m-%d-%Y")
    start = (datetime.now() - timedelta(days=days_back)).strftime("%m-%d-%Y")
    char_params = "&".join([f"characteristicName={c.replace(' ', '%20')}" for c in contaminants])


    url = (
        "https://www.waterqualitydata.us/data/Result/search"
        f"?statecode=US:26"
        f"&{char_params}"
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
        "CharacteristicName",
        "ResultMeasureValue",
        "ResultMeasure/MeasureUnitCode",
    ]
    return df[[c for c in keep if c in df.columns]]


def fetch_michigan_stations(contaminants: list) -> pd.DataFrame:
    char_params = "&".join([f"characteristicName={c.replace(' ', '%20')}" for c in contaminants])

    url = (
        "https://www.waterqualitydata.us/data/Station/search"
        f"?statecode=US:26"
        f"&{char_params}"
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
    return df[[c for c in keep if c in df.columns]].drop_duplicates()


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
    print("Fetching contaminant data...")
    results = fetch_michigan_contaminants(CONTAMINANTS, days_back=365)

    print("Fetching stations...")
    stations = fetch_michigan_stations(CONTAMINANTS)
    stations = filter_out_stream_sites(stations)

    print("Matching beaches to stations...")
    matches = match_beaches_to_stations(COASTCAST_SAMPLE, stations, max_miles=1.0)

    beach_contaminant_map = {}
    for match in matches:
        if not match["matched"]:
            continue
        beach_id = match["beach_id"]
        station_id = match["station_id"]

        station_rows = results[
            results["MonitoringLocationIdentifier"] == station_id
        ]

        latest = (
            station_rows.sort_values("ActivityStartDate", ascending=False)
            .groupby("CharacteristicName")
            .first()
            .reset_index()
        )

        beach_contaminant_map[beach_id] = latest.to_dict(orient="records")

    with open("app/data/beach_contaminant_map.json", "w") as f:
        json.dump(beach_contaminant_map, f, indent=2, default=str)

    print(f"Done. {len(beach_contaminant_map)} beaches mapped.")