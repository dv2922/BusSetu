# BusSetu real-data ingestion plan

Do not scrape live GSRTC booking pages from the frontend. Build a backend-only data adapter that:

1. Reads `app/data_sources/popular_route_targets.csv`.
2. Queries each source/destination/date pair in a controlled backend job.
3. Stores normalized results into a database/cache.
4. Serves BusSetu from the cache.

Reason: booking/timetable pages can change, may use anti-bot protections, and should not be hit repeatedly for every user search.

Current MVP intentionally uses seeded demo data. Next implementation step is a `gsrtc_adapter.py` that converts official/partner search results into this normalized trip shape:

```json
{
  "from": "Ahmedabad",
  "to": "Vadodara",
  "departure": "08:15",
  "arrival": "10:15",
  "bus_type": "Express",
  "fare": 160,
  "service_name": "Ahmedabad-Vadodara Express",
  "source_url": "..."
}
```

Recommended first routes are listed in `popular_route_targets.csv`.
