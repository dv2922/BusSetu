"""Load scraped GSRTC CSV cache files into BusSetu service format.

Expected CSV columns:
From_Station,To_Station,Departure_Time,Arrival_Time,Bus_Category,Fare_INR
"""

import csv
import glob
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

STOP_REPLACEMENTS = {
    "ahmedabad": "Ahmedabad",
    "baroda": "Baroda CBS",
    "vadodara": "Vadodara",
    "rajkot": "Rajkot",
    "surat": "Surat",
    "navsari": "Navsari",
    "nadiad": "Nadiad",
    "bharuch": "Bharuch",
    "mehsana": "Mehsana",
    "patan": "Patan",
    "bhuj": "Bhuj",
    "junagadh": "Junagadh",
    "dwarka": "Dwarka",
}


def normalize_csv_stop(name: str) -> str:
    cleaned = str(name or "").strip().replace("_", " ").lower()
    if cleaned in STOP_REPLACEMENTS:
        return STOP_REPLACEMENTS[cleaned]
    return " ".join(word.capitalize() for word in cleaned.split())


def normalize_time(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "00:00"
    # Accept HH:MM, H:MM, or HH:MM:SS and output HH:MM.
    parts = raw.split(":")
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    return f"{hour:02d}:{minute:02d}"


def normalize_fare(value: str) -> int:
    try:
        return int(round(float(str(value).strip())))
    except (TypeError, ValueError):
        return 0


def load_csv_services() -> List[Dict]:
    services: List[Dict] = []
    csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))

    for path in csv_files:
        file_label = os.path.splitext(os.path.basename(path))[0]

        with open(path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for index, row in enumerate(reader, start=1):
                source = normalize_csv_stop(row.get("From_Station", ""))
                destination = normalize_csv_stop(row.get("To_Station", ""))
                departure = normalize_time(row.get("Departure_Time", ""))
                arrival = normalize_time(row.get("Arrival_Time", ""))
                bus_type = str(row.get("Bus_Category", "GSRTC")).strip() or "GSRTC"
                fare = normalize_fare(row.get("Fare_INR", "0"))

                if not source or not destination or source == destination:
                    continue

                services.append(
                    {
                        "service_name": f"{source}-{destination} {bus_type} #{index}",
                        "bus_type": bus_type,
                        "runs_daily": True,
                        "fixed_fare": fare,
                        "source_file": file_label,
                        "stops": [
                            (source, departure),
                            (destination, arrival),
                        ],
                    }
                )

    return services
