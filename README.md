# MichiganWaterAPI

The API behind CoastCast. Pulls weather, wave, and alert data from the National Weather Service and NDBC buoy APIs for five Michigan beaches, combines it, and serves it to the frontend. Built with FastAPI and deployed on Render.

[View Frontend on GitHub](https://github.com/jaidenhenley/Swift-MichiganAPIWeather)

## Stack

Python, FastAPI, HTTPX, asyncio, Render

## Endpoints

- `GET /beaches` returns all five beaches with basic info
- `GET /beaches/{id}` returns full detail for a single beach including current conditions, forecast, wave data, and active alerts

## Architecture

I built this as the backend of a CoastCast.

**Data flow.** Each beach maps to a set of NWS coordinates and a nearby NDBC buoy station. When `/beaches/{id}` gets called, the service pulls parallel requests with `asyncio.gather` to pull weather forecasts, current observations, active alerts, and buoy readings all at the same time. Everything comes back and gets stitched into a single response so the frontend only has to make one call.

**NWS service.** Handles forecast and observation data. Hits the NWS points endpoint to get the forecast URL for a given set of coordinates, then fetches the forecast and current conditions.

**NDBC service.** Pulls buoy data for wave height, water temperature, and wind readings from the nearest station mapped to each beach.

**Alerts.** NWS alerts are fetched per beach coordinates and included in the detail response if any are active.

**No database.** Nothing is stored. Every response is assembled live from the upstream APIs. The app is a passthrough that does the work of combining multiple sources so the frontend doesn't have to.

## Setup

```bash
git clone https://github.com/jaidenhenley/Python-MichiganWaterAPI.git
cd Python-MichiganWaterAPI
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Hit `/docs` for the auto-generated Swagger UI.

## Deployment

Deployed on Render. Ran into some issues during deployment like missing dependencies, uvicorn misconfiguration, a committed `.venv`, and a macOS case-sensitivity git issue with the `app/` folder. Worked through all of them.

## Developers

Jaiden Henley | [Portfolio](https://jaidenhenley.github.io/JaidenHenleyPort/) | [LinkedIn](https://www.linkedin.com/in/jaiden-henley) | [jaidenhenleydev@gmail.com](mailto:jaidenhenleydev@gmail.com)

George Clinkscales | [Portfolio](https://geoclink.github.io/portfolio/) | [LinkedIn](https://www.linkedin.com/in/george-clinkscales/) | [1lclink2@att.net](mailto:1lclink2@att.net)
