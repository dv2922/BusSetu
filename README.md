# BusSetu MVP v0.6

Connected GSRTC-style bus route planner MVP.

## What changed in v0.6

- Backend now uses **service-level dummy data** instead of only `from -> to` trips.
- A long service can be used as a **direct segment**.
  - Example: `Ahmedabad -> Navsari Volvo` can be shown for `Nadiad -> Navsari` if Nadiad and Navsari are both in its stop sequence.
- One-transfer search also uses service segments.
  - Example: `Nadiad -> Baroda CBS` by Volvo + `Baroda CBS -> Saputara` by Gurjarnagari.
- Frontend still has searchable dropdowns to prevent illegal stop input.
- Dates remain restricted to today through today + 15 days.

## Run backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

Try:

```text
http://localhost:8000/api/search?from=Nadiad&to=Navsari&date=<today-or-within-15-days>
http://localhost:8000/api/search?from=Nadiad&to=Saputara&date=<today-or-within-15-days>
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Data note

All timings/fares are dummy/assumed for development. Replace entries in:

```text
backend/app/seed_data.py
```

with verified GSRTC screenshots/API/cache data.


## v0.6 UI fix

- Dropdown no longer shows red validation while the user is still typing.
- Exact typed stop names are accepted without requiring an extra click.
- Enter selects the first suggestion.
- Search helper text shortened to prevent overlap with suggestions.


## v0.6 UI polish
- Professional blue/white gradient background.
- Built-in SVG bus logo mark.
- Removed MVP wording from visible homepage.
- Search card, dropdowns, route cards and mobile layout polished.

