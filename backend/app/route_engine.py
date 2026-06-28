from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .seed_data import ALIASES, HUBS, SERVICES as SEED_SERVICES, STOPS
from .csv_loader import load_csv_services

SERVICES = SEED_SERVICES + load_csv_services()

MIN_TRANSFER = timedelta(minutes=45)
MAX_TRANSFER = timedelta(hours=4)

# Rough road-distance approximation from stop sequence index/time.
# This is only for MVP demo fare estimates until real fare data is imported.
FARE_MINIMUM = 25

def normalize_stop(stop: str) -> str:
    raw = stop.strip()
    key = raw.lower()
    if key in ALIASES:
        return ALIASES[key]
    for known in STOPS:
        if known.lower() == key:
            return known
    return " ".join(word.capitalize() for word in raw.split())


def parse_time(date: str, hhmm: str) -> datetime:
    return datetime.fromisoformat(f"{date}T{hhmm}:00")


def minutes_between(date: str, departure: str, arrival: str) -> int:
    d = parse_time(date, departure)
    a = parse_time(date, arrival)
    if a < d:
        a += timedelta(days=1)
    return int((a - d).total_seconds() // 60)


def estimate_fare(service: Dict, duration_minutes: int) -> int:
    if "fixed_fare" in service:
        return int(float(service["fixed_fare"]))

    # MVP approximation: longer and premium services cost more.
    # Assumption: average road speed ~45 km/h.
    approx_km = max(8, duration_minutes * 0.75)
    factor = service.get("fare_per_km_factor", 1.25)
    fare = max(FARE_MINIMUM, round(approx_km * factor / 5) * 5)
    return int(fare)


def stop_index_map(service: Dict) -> Dict[str, int]:
    return {normalize_stop(stop): idx for idx, (stop, _time) in enumerate(service["stops"])}


def segment_from_service(service: Dict, source: str, destination: str, date: str) -> Optional[Dict]:
    source = normalize_stop(source)
    destination = normalize_stop(destination)
    index_map = stop_index_map(service)

    if source not in index_map or destination not in index_map:
        return None

    src_idx = index_map[source]
    dst_idx = index_map[destination]
    if src_idx >= dst_idx:
        return None

    source_stop, departure = service["stops"][src_idx]
    destination_stop, arrival = service["stops"][dst_idx]
    duration = minutes_between(date, departure, arrival)

    return {
        "from": normalize_stop(source_stop),
        "to": normalize_stop(destination_stop),
        "departure": departure,
        "arrival": arrival,
        "bus_type": service["bus_type"],
        "fare": estimate_fare(service, duration),
        "service_name": service["service_name"],
        "service_origin": normalize_stop(service["stops"][0][0]),
        "service_destination": normalize_stop(service["stops"][-1][0]),
        "runs_daily": service.get("runs_daily", True),
        "is_segment": not (
            normalize_stop(service["stops"][0][0]) == source and
            normalize_stop(service["stops"][-1][0]) == destination
        ),
        "duration_minutes": duration,
    }


def serialize_leg(segment: Dict) -> Dict:
    return {
        "from": segment["from"],
        "to": segment["to"],
        "departure": segment["departure"],
        "arrival": segment["arrival"],
        "bus_type": segment["bus_type"],
        "fare": segment["fare"],
        "service_name": segment["service_name"],
        "service_origin": segment.get("service_origin"),
        "service_destination": segment.get("service_destination"),
        "runs_daily": segment.get("runs_daily", True),
        "is_segment": segment.get("is_segment", False),
    }


def search_segments(source: str, destination: str, date: str) -> List[Dict]:
    source = normalize_stop(source)
    destination = normalize_stop(destination)
    results: List[Dict] = []
    for service in SERVICES:
        segment = segment_from_service(service, source, destination, date)
        if segment:
            results.append(segment)
    return sorted(results, key=lambda s: (s["departure"], s["arrival"], s["service_name"]))


def risk_label(wait: timedelta) -> str:
    minutes = wait.total_seconds() / 60
    if minutes < 45:
        return "High"
    if minutes <= 90:
        return "Low"
    return "Medium"


def risk_penalty(risk: str) -> int:
    return {"Low": 0, "Medium": 45, "High": 120}.get(risk, 90)


def bus_type_penalty(legs: List[Dict]) -> int:
    # Favor Volvo/Gurjarnagari slightly in rankings, since user asked for premium regular services.
    penalty = 0
    for leg in legs:
        bus_type = leg["bus_type"].lower()
        if "volvo" in bus_type:
            penalty -= 35
        elif "gurjarnagari" in bus_type:
            penalty -= 15
        elif "local" in bus_type:
            penalty += 30
    return penalty


def calculate_score(total_minutes: int, waiting_minutes: int, transfers: int, risk: str, legs: List[Dict]) -> float:
    return (
        total_minutes * 1.0
        + waiting_minutes * 0.5
        + transfers * 120
        + risk_penalty(risk)
        + bus_type_penalty(legs)
    )


def find_routes(source: str, destination: str, date: str) -> Dict:
    source = normalize_stop(source)
    destination = normalize_stop(destination)

    # Direct here means either exact service endpoint OR useful segment inside a longer regular service.
    direct_segments = search_segments(source, destination, date)
    direct_routes = [serialize_leg(segment) for segment in direct_segments]

    connected_routes = []
    for hub in HUBS:
        hub = normalize_stop(hub)
        if hub in {source, destination}:
            continue

        first_leg = search_segments(source, hub, date)
        second_leg = search_segments(hub, destination, date)

        for bus1 in first_leg:
            bus1_arrival = parse_time(date, bus1["arrival"])
            bus1_departure = parse_time(date, bus1["departure"])

            for bus2 in second_leg:
                # Avoid silly same-service transfers. If one service already covers source -> destination,
                # it should appear as a direct segment, not a forced connection.
                if bus1["service_name"] == bus2["service_name"]:
                    continue

                bus2_departure = parse_time(date, bus2["departure"])
                bus2_arrival = parse_time(date, bus2["arrival"])
                if bus2_arrival < bus2_departure:
                    bus2_arrival += timedelta(days=1)

                wait = bus2_departure - bus1_arrival
                if MIN_TRANSFER <= wait <= MAX_TRANSFER:
                    total = bus2_arrival - bus1_departure
                    total_minutes = int(total.total_seconds() / 60)
                    waiting_minutes = int(wait.total_seconds() / 60)
                    risk = risk_label(wait)
                    fare = int(bus1["fare"] + bus2["fare"])
                    legs = [bus1, bus2]
                    score = calculate_score(total_minutes, waiting_minutes, 1, risk, legs)

                    connected_routes.append({
                        "transfer": hub,
                        "total_duration_minutes": total_minutes,
                        "waiting_minutes": waiting_minutes,
                        "risk": risk,
                        "score": score,
                        "estimated_fare": fare,
                        "legs": [serialize_leg(bus1), serialize_leg(bus2)],
                    })

    connected_routes = sorted(connected_routes, key=lambda r: r["score"])

    if not direct_routes and not connected_routes:
        message = "No direct segment or safe one-transfer route found in current demo data."
    elif direct_routes:
        message = "Direct usable service segment found. Connected alternatives are also shown if available."
    else:
        message = "No direct usable segment found. Showing safe connected routes."

    return {
        "source": source,
        "destination": destination,
        "date": date,
        "direct_routes": direct_routes,
        "connected_routes": connected_routes,
        "message": message,
        "data_note": "Demo data uses assumed regular service stop-times. Verify with GSRTC screenshots before public use.",
    }
