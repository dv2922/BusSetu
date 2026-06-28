"use client";

import { useEffect, useMemo, useState } from "react";

type Leg = {
  from: string;
  to: string;
  departure: string;
  arrival: string;
  bus_type: string;
  fare: number;
  service_name: string;
  service_origin?: string;
  service_destination?: string;
  runs_daily?: boolean;
  is_segment?: boolean;
};

type ConnectedRoute = {
  transfer: string;
  total_duration_minutes: number;
  waiting_minutes: number;
  risk: string;
  score: number;
  estimated_fare: number;
  legs: Leg[];
};

type SearchResponse = {
  source: string;
  destination: string;
  date: string;
  direct_routes: Leg[];
  connected_routes: ConnectedRoute[];
  message?: string;
  error?: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

function formatDuration(minutes: number) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h} hr ${m} min`;
}

function normalize(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function canonicalStop(value: string, stops: string[]) {
  return stops.find((stop) => normalize(stop) === normalize(value)) || value;
}

function BusSetuLogo() {
  return (
    <div className="logo-wrap" aria-label="BusSetu logo">
      <div className="logo-mark">
        <svg viewBox="0 0 48 48" role="img" aria-hidden="true">
          <path d="M13 8h22c4.4 0 8 3.6 8 8v13c0 3.3-2.7 6-6 6h-1v2.5a2.5 2.5 0 0 1-5 0V35H17v2.5a2.5 2.5 0 0 1-5 0V35h-1c-3.3 0-6-2.7-6-6V16c0-4.4 3.6-8 8-8Z" />
          <path d="M11 16c0-1.1.9-2 2-2h22c1.1 0 2 .9 2 2v7H11v-7Z" className="logo-window" />
          <circle cx="15.5" cy="30" r="2" className="logo-dot" />
          <circle cx="32.5" cy="30" r="2" className="logo-dot" />
          <path d="M18 29h12" className="logo-line" />
        </svg>
      </div>
      <div>
        <span className="logo-name">BusSetu</span>
        <span className="logo-sub">Connected GSRTC Route planner</span>
      </div>
    </div>
  );
}

function StopInput({
  label,
  value,
  onChange,
  stops,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  stops: string[];
  placeholder: string;
}) {
  const [open, setOpen] = useState(false);
  const [touched, setTouched] = useState(false);

  const suggestions = useMemo(() => {
    const q = normalize(value);
    if (!q) return stops.slice(0, 8);
    return stops
      .filter((stop) => normalize(stop).includes(q))
      .sort((a, b) => {
        const aq = normalize(a).startsWith(q) ? 0 : 1;
        const bq = normalize(b).startsWith(q) ? 0 : 1;
        return aq - bq || a.localeCompare(b);
      })
      .slice(0, 10);
  }, [value, stops]);

  const exactMatch = stops.some((stop) => normalize(stop) === normalize(value));
  const showInvalid = touched && value.length > 0 && stops.length > 0 && !exactMatch;

  function selectStop(stop: string) {
    onChange(stop);
    setTouched(false);
    setOpen(false);
  }

  return (
    <div className="field combo">
      <label>{label}</label>
      <input
        value={value}
        placeholder={placeholder}
        autoComplete="off"
        onFocus={() => {
          setOpen(true);
          setTouched(false);
        }}
        onBlur={() => {
          setTimeout(() => setOpen(false), 120);
          setTouched(true);
        }}
        onChange={(e) => {
          onChange(e.target.value);
          setTouched(false);
          setOpen(true);
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" && suggestions.length > 0 && !exactMatch) {
            e.preventDefault();
            selectStop(suggestions[0]);
          }
        }}
        className={showInvalid ? "invalid" : ""}
      />
      {open && suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((stop) => (
            <button type="button" key={stop} onMouseDown={() => selectStop(stop)}>
              {stop}
            </button>
          ))}
        </div>
      )}
      {showInvalid && <small>Select one stop from the dropdown.</small>}
    </div>
  );
}

function DirectRouteCard({ leg }: { leg: Leg }) {
  return (
    <div className="card route-card">
      <div className="route-title">
        <h3>{leg.from} → {leg.to}</h3>
        <span className="badge green">{leg.is_segment ? "Direct segment" : "Direct"}</span>
      </div>
      <div className="timeline">
        <div className="leg">
          <strong>{leg.service_name}</strong>
          <div className="meta">{leg.departure} → {leg.arrival} · {leg.bus_type} · ₹{leg.fare}</div>
          {leg.is_segment && <div className="meta">Full service: {leg.service_origin} → {leg.service_destination}</div>}
        </div>
      </div>
    </div>
  );
}

function ConnectedRouteCard({ route, index }: { route: ConnectedRoute; index: number }) {
  const riskClass = route.risk === "Low" ? "green" : route.risk === "Medium" ? "amber" : "red";
  return (
    <div className="card route-card">
      <div className="route-title">
        <div>
          <p className="eyebrow">Option {index + 1}</p>
          <h3>{route.legs[0].from} → {route.transfer} → {route.legs[1].to}</h3>
        </div>
        <span className={`badge ${riskClass}`}>Risk: {route.risk}</span>
      </div>
      <div className="stats">
        <div><strong>{formatDuration(route.total_duration_minutes)}</strong><span>Total</span></div>
        <div><strong>{formatDuration(route.waiting_minutes)}</strong><span>Transfer wait</span></div>
        <div><strong>₹{route.estimated_fare}</strong><span>Fare estimate</span></div>
      </div>
      <div className="timeline">
        <div className="leg">
          <strong>{route.legs[0].departure} · {route.legs[0].from} → {route.legs[0].to}</strong>
          <div className="meta">Arrives {route.legs[0].arrival} · {route.legs[0].service_name} · ₹{route.legs[0].fare}</div>
          {route.legs[0].is_segment && <div className="meta">Full service: {route.legs[0].service_origin} → {route.legs[0].service_destination}</div>}
        </div>
        <div className="leg transfer">
          <strong>Change at {route.transfer}</strong>
          <div className="meta">Safe buffer: {formatDuration(route.waiting_minutes)}</div>
        </div>
        <div className="leg">
          <strong>{route.legs[1].departure} · {route.legs[1].from} → {route.legs[1].to}</strong>
          <div className="meta">Arrives {route.legs[1].arrival} · {route.legs[1].service_name} · ₹{route.legs[1].fare}</div>
          {route.legs[1].is_segment && <div className="meta">Full service: {route.legs[1].service_origin} → {route.legs[1].service_destination}</div>}
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [stops, setStops] = useState<string[]>([]);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");

  function todayIso() {
    return new Date().toISOString().slice(0, 10);
  }

  function maxDateIso(days = 15) {
    const d = new Date();
    d.setDate(d.getDate() + days);
    return d.toISOString().slice(0, 10);
  }

  const minDate = todayIso();
  const maxDate = maxDateIso(15);
  const [date, setDate] = useState(minDate);
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/stops`)
      .then((res) => res.json())
      .then((json) => setStops(json.stops || []))
      .catch(() => setError("Backend is not reachable. Start FastAPI on http://localhost:8000."));
  }, []);

  const validFrom = stops.some((stop) => normalize(stop) === normalize(from));
  const validTo = stops.some((stop) => normalize(stop) === normalize(to));
  const validDate = !!date && date >= minDate && date <= maxDate;
  const canSearch = validFrom && validTo && validDate && !loading;

  async function search() {
    if (!canSearch) {
      setError("Select valid From/To stops and choose a journey date between today and the next 15 days.");
      return;
    }

    setLoading(true);
    setError("");
    setData(null);
    try {
      const params = new URLSearchParams({ from: canonicalStop(from, stops), to: canonicalStop(to, stops), date });
      const res = await fetch(`${API_BASE}/api/search?${params.toString()}`);
      const json = await res.json();
      if (!res.ok || json.error) throw new Error(json.error || "Search failed");
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not search routes.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <BusSetuLogo />
          <p className="eyebrow">GSRTC connected route planner</p>
          <h1>Find a route for non-direct connections.</h1>
          <p className="hero-text">BusSetu checks direct services, long-route boarding segments and safe one-stop connections.</p>
        </div>
        <div className="hero-card">
          <span className="mini-icon">🚌</span>
          <strong>Direct, segment and one-stop journeys</strong>
          <p>Built for recurring GSRTC Volvo, Gurjarnagari and Express service combinations across Gujarat.</p>
        </div>
      </section>

      <section className="card search-card">
        <div className="form-grid">
          <StopInput label="From" value={from} onChange={setFrom} stops={stops} placeholder="Type Nadiad, Baroda, Botad..." />
          <StopInput label="To" value={to} onChange={setTo} stops={stops} placeholder="Type Saputara, Surat, Somnath..." />
          <div className="field">
            <label>Date</label>
            <input type="date" min={minDate} max={maxDate} value={date} onChange={(e) => setDate(e.target.value)} />
            {!validDate && date && <small>Date must be between today and the next 15 days.</small>}
          </div>
          <button onClick={search} disabled={!canSearch}>{loading ? "Searching..." : "Find Route"}</button>
        </div>
        {error && <p className="message error">{error}</p>}
      </section>

      {data && (
        <section className="results">
          <div className="results-head">
            <div>
              <p className="eyebrow">Search result</p>
              <h2>{data.source} → {data.destination}</h2>
            </div>
            <span className="badge">{data.date}</span>
          </div>
          {data.message && <p className="message">{data.message}</p>}

          {data.direct_routes.length > 0 && <h2>Direct Routes</h2>}
          {data.direct_routes.map((leg, i) => <DirectRouteCard key={`direct-${i}`} leg={leg} />)}

          {data.connected_routes.length > 0 && <h2>Connected Routes</h2>}
          {data.connected_routes.map((route, i) => <ConnectedRouteCard key={`connected-${i}`} route={route} index={i} />)}
        </section>
      )}
    </main>
  );
}
