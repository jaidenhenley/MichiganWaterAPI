import httpx

MICHIGAN_BEACH_ZONES = [
    "LMZ644", "LMZ645", "LMZ646",
    "LMZ740", "LMZ741", "LMZ742",
    "LHZ421", "LHZ422", "LHZ423",
]

BEACH_ALERT_TYPES = [
    "Beach Hazard Statement",
    "Rip Current Statement",
    "Small Craft Advisory",
    "Gale Warning",
    "Storm Warning",
    "Special Marine Warning",
    "High Surf Advisory",
]


async def fetch_nws_beach_alerts(zones: list[str]) -> list[dict]:
    zone_str = ",".join(zones)
    url = f"https://api.weather.gov/alerts/active?zone={zone_str}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers={"User-Agent": "CoastCast/1.0"})

    if response.status_code != 200:
        return []

    data = response.json()
    features = data.get("features", [])

    alerts = []
    for feature in features:
        props = feature.get("properties", {})
        event = props.get("event", "")
        if event in BEACH_ALERT_TYPES:
            alerts.append({
                "event": event,
                "headline": props.get("headline", ""),
                "severity": props.get("severity", ""),
                "urgency": props.get("urgency", ""),
                "effective": props.get("effective", ""),
                "expires": props.get("expires", ""),
            })

    return alerts


async def get_beach_alerts_safe() -> list[dict]:
    try:
        return await fetch_nws_beach_alerts(MICHIGAN_BEACH_ZONES)
    except Exception as e:
        print(f"[NWS] Error fetching beach alerts: {e}")
        return []
