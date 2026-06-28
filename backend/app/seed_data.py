# BusSetu MVP static data.
# IMPORTANT: These are assumed/demo timings for product development only.
# Replace with verified GSRTC screenshots/API/cache entries as we collect real data.

STOPS = [
    "Ahmedabad", "Ahmedabad Ranip", "Ahmedabad Nehrunagar", "Anand", "Anjar", "Ahwa",
    "Baroda CBS", "Bardoli", "Bharuch", "Bhavnagar", "Bhuj", "Bilimora", "Bochasan",
    "Bopal", "Borsad", "Botad", "Chhani", "Dahod", "Diu", "Dwarka", "Gandhidham",
    "Godhra", "Himmatnagar", "Jamnagar", "Junagadh", "Kheda", "Mehsana", "Morbi",
    "Nadiad", "Navsari", "Palanpur", "Patan", "Rajkot", "Saputara", "Somnath",
    "Statue of Unity", "Surat", "Surat CBS", "Una", "Vadodara", "Valsad", "Veraval",
    "Vyara"
]

ALIASES = {
    "baroda": "Vadodara",
    "baroda cbs": "Baroda CBS",
    "vadodra": "Vadodara",
    "vadodara cbs": "Baroda CBS",
    "amdavad": "Ahmedabad",
    "ahemdabad": "Ahmedabad",
    "ahmedabad cbs": "Ahmedabad",
    "ranip": "Ahmedabad Ranip",
    "surat central": "Surat CBS",
    "saputara hill station": "Saputara",
    "statue": "Statue of Unity",
    "sou": "Statue of Unity",
    "veraval somnath": "Somnath",
    "kutch": "Bhuj",
    "kachchh": "Bhuj",
    "katch": "Bhuj",
}

# Search hub priority for one-transfer routing.
HUBS = [
    "Vadodara", "Baroda CBS", "Surat", "Surat CBS", "Navsari", "Bilimora", "Valsad",
    "Bharuch", "Anand", "Nadiad", "Ahmedabad", "Ahmedabad Ranip", "Vyara", "Ahwa",
    "Rajkot", "Bhavnagar", "Mehsana", "Patan", "Palanpur", "Godhra", "Dahod",
    "Junagadh", "Jamnagar", "Bhuj", "Gandhidham", "Botad"
]

# Service-level data: one service can be boarded/deboarded at intermediate stops.
# stop_times format: (stop_name, departure_time). Same-day MVP assumption.
SERVICES = [
    {
        "service_name": "Ahmedabad-Navsari Volvo",
        "bus_type": "Volvo",
        "runs_daily": True,
        "fare_per_km_factor": 2.1,
        "stops": [
            ("Ahmedabad", "06:00"),
            ("Nadiad", "07:15"),
            ("Anand", "07:45"),
            ("Baroda CBS", "08:35"),
            ("Bharuch", "10:00"),
            ("Surat", "11:25"),
            ("Navsari", "12:15"),
        ],
    },
    {
        "service_name": "Gandhinagar-Ahmedabad-Navsari Volvo",
        "bus_type": "Volvo",
        "runs_daily": True,
        "fare_per_km_factor": 2.1,
        "stops": [
            ("Ahmedabad Ranip", "07:30"),
            ("Ahmedabad", "08:00"),
            ("Nadiad", "09:10"),
            ("Baroda CBS", "10:20"),
            ("Bharuch", "11:45"),
            ("Surat", "13:05"),
            ("Navsari", "13:55"),
        ],
    },
    {
        "service_name": "Rajkot-Vadodara Volvo",
        "bus_type": "Volvo",
        "runs_daily": True,
        "fare_per_km_factor": 2.1,
        "stops": [
            ("Rajkot", "05:30"),
            ("Ahmedabad", "09:45"),
            ("Nadiad", "10:55"),
            ("Anand", "11:25"),
            ("Baroda CBS", "12:15"),
        ],
    },
    {
        "service_name": "Rajkot-Vadodara Volvo Evening",
        "bus_type": "Volvo",
        "runs_daily": True,
        "fare_per_km_factor": 2.1,
        "stops": [
            ("Rajkot", "08:00"),
            ("Ahmedabad", "12:20"),
            ("Nadiad", "13:35"),
            ("Anand", "14:05"),
            ("Baroda CBS", "14:55"),
        ],
    },
    {
        "service_name": "Ahmedabad-Surat Volvo",
        "bus_type": "Volvo",
        "runs_daily": True,
        "fare_per_km_factor": 2.1,
        "stops": [
            ("Ahmedabad", "05:45"),
            ("Nadiad", "06:55"),
            ("Baroda CBS", "08:00"),
            ("Bharuch", "09:25"),
            ("Surat", "10:45"),
        ],
    },
    {
        "service_name": "Ahmedabad-Surat Gurjarnagari",
        "bus_type": "Gurjarnagari",
        "runs_daily": True,
        "fare_per_km_factor": 1.55,
        "stops": [
            ("Ahmedabad", "09:30"),
            ("Nadiad", "10:45"),
            ("Anand", "11:10"),
            ("Baroda CBS", "12:05"),
            ("Bharuch", "13:40"),
            ("Surat", "15:10"),
        ],
    },
    {
        "service_name": "Vadodara-Saputara Gurjarnagari",
        "bus_type": "Gurjarnagari",
        "runs_daily": True,
        "fare_per_km_factor": 1.55,
        "stops": [
            ("Baroda CBS", "10:15"),
            ("Bharuch", "11:45"),
            ("Surat", "13:15"),
            ("Navsari", "14:05"),
            ("Vyara", "15:05"),
            ("Ahwa", "16:05"),
            ("Saputara", "16:40"),
        ],
    },
    {
        "service_name": "Surat-Saputara Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Surat", "11:15"),
            ("Navsari", "12:05"),
            ("Bardoli", "12:50"),
            ("Vyara", "13:40"),
            ("Ahwa", "15:30"),
            ("Saputara", "16:30"),
        ],
    },
    {
        "service_name": "Navsari-Saputara Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Navsari", "10:30"),
            ("Bilimora", "11:10"),
            ("Vyara", "12:55"),
            ("Ahwa", "14:15"),
            ("Saputara", "15:00"),
        ],
    },
    {
        "service_name": "Ahmedabad-Rajkot Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Ahmedabad", "06:30"),
            ("Botad", "09:20"),
            ("Rajkot", "12:00"),
        ],
    },
    {
        "service_name": "Ahmedabad-Dwarka Sleeper",
        "bus_type": "Sleeper",
        "runs_daily": True,
        "fare_per_km_factor": 1.75,
        "stops": [
            ("Ahmedabad", "05:45"),
            ("Rajkot", "11:15"),
            ("Jamnagar", "13:45"),
            ("Dwarka", "17:45"),
        ],
    },
    {
        "service_name": "Ahmedabad-Bhuj Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Ahmedabad", "06:00"),
            ("Mehsana", "07:50"),
            ("Patan", "09:05"),
            ("Gandhidham", "13:10"),
            ("Bhuj", "14:30"),
        ],
    },
    {
        "service_name": "Ahmedabad-Patan Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Ahmedabad", "08:00"),
            ("Mehsana", "09:40"),
            ("Patan", "11:10"),
            ("Palanpur", "13:00"),
        ],
    },
    {
        "service_name": "Rajkot-Junagadh-Somnath Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Rajkot", "08:00"),
            ("Junagadh", "10:15"),
            ("Veraval", "13:05"),
            ("Somnath", "13:30"),
        ],
    },
    {
        "service_name": "Surat-Statue of Unity Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Surat", "07:30"),
            ("Bharuch", "09:40"),
            ("Vadodara", "11:20"),
            ("Statue of Unity", "12:30"),
        ],
    },
    {
        "service_name": "Nadiad-Bochasan-Botad Express",
        "bus_type": "Express",
        "runs_daily": True,
        "fare_per_km_factor": 1.25,
        "stops": [
            ("Nadiad", "06:20"),
            ("Bochasan", "07:30"),
            ("Borsad", "08:10"),
            ("Botad", "11:45"),
        ],
    },
]
