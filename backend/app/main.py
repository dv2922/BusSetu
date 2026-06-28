from datetime import date as date_cls, timedelta

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .route_engine import SERVICES, find_routes
from .seed_data import STOPS

app = FastAPI(
    title="BusSetu API",
    description="Connected GSRTC-style bus route planner MVP",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_journey_date(value: str) -> None:
    try:
        journey_date = date_cls.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Date must use YYYY-MM-DD format.") from exc

    today = date_cls.today()
    max_date = today + timedelta(days=15)
    if journey_date < today:
        raise HTTPException(status_code=400, detail="Past dates are not allowed.")
    if journey_date > max_date:
        raise HTTPException(status_code=400, detail="Journey date cannot be more than 15 days from today.")


@app.get("/")
def health_check():
    return {"status": "ok", "app": "BusSetu API"}


@app.get("/api/stops")
def get_stops():
    all_stops = set(STOPS)

    for service in SERVICES:
        for stop in service.get("stops", []):
            if stop and stop[0]:
                all_stops.add(stop[0])

    return {"stops": sorted(all_stops)}


@app.get("/api/search")
def search_routes(
    from_stop: str = Query(..., alias="from"),
    to_stop: str = Query(..., alias="to"),
    date: str = Query(..., description="Journey date in YYYY-MM-DD format. Allowed range: today to today + 15 days."),
):
    validate_journey_date(date)
    return find_routes(from_stop, to_stop, date)
