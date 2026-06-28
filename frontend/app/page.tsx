"use client";

import { useEffect, useMemo, useState } from "react";
import { getStops, searchRoutes } from "@/lib/api";

type Leg = {
  from: string;
  to: string;
  departure: string;
  arrival: string;
  bus_type: string;
  fare: number;
  service_name: string;
};

type RouteOption = {
  transfer?: string;
  total_duration_minutes: number;
  waiting_minutes?: number;
  risk?: string;
  score?: number;
  estimated_fare: number;
  legs: Leg[];
};

type SearchResponse = {
  source: string;
  destination: string;
  date: string;
  direct_routes: RouteOption[];
  connected_routes: RouteOption[];
  message: string;
};

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function maxDateISO() {
  const d = new Date();
  d.setDate(d.getDate() + 15);
  return d.toISOString().slice(0, 10);
}

function minutesToText(minutes: number) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  if (h && m) return `${h}h ${m}m`;
  if (h) return `${h}h`;
  return `${m}m`;
}

export default function Home() {
  const [stops, setStops] = useState<string[]>([]);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [date, setDate] = useState(todayISO());
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loadingStops, setLoadingStops] = useState(true);
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStops() {
      try {
        setLoadingStops(true);
        const data = await getStops();
        setStops(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Failed to load stops:", err);
        setStops([]);
        setError("Could not load stations. Please refresh.");
      } finally {
        setLoadingStops(false);
      }
    }

    loadStops();
  }, []);

  const fromSuggestions = useMemo(() => {
    if (!from.trim()) return stops.slice(0, 8);
    return stops
      .filter((s) => s.toLowerCase().includes(from.toLowerCase()))
      .slice(0, 8);
  }, [from, stops]);

  const toSuggestions = useMemo(() => {
    if (!to.trim()) return stops.slice(0, 8);
    return stops
      .filter((s) => s.toLowerCase().includes(to.toLowerCase()))
      .slice(0, 8);
  }, [to, stops]);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResults(null);

    if (!stops.includes(from)) {
      setError("Please select a valid From station from dropdown.");
      return;
    }

    if (!stops.includes(to)) {
      setError("Please select a valid To station from dropdown.");
      return;
    }

    if (from === to) {
      setError("From and To station cannot be same.");
      return;
    }

    if (date < todayISO() || date > maxDateISO()) {
      setError("Date must be from today to next 15 days only.");
      return;
    }

    try {
      setLoadingSearch(true);
      const data = await searchRoutes(from, to, date);
      setResults(data);
    } catch (err) {
      console.error("Search failed:", err);
      setError("Search failed. Please check backend connection.");
    } finally {
      setLoadingSearch(false);
    }
  }

  const allRoutes = results
    ? [...(results.direct_routes || []), ...(results.connected_routes || [])]
    : [];

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-sky-100 px-4 py-8 text-slate-900">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600 text-3xl text-white shadow-lg">
            🚌
          </div>

          <h1 className="text-4xl font-bold tracking-tight text-blue-950">
            BusSetu
          </h1>

          <p className="mt-2 text-lg font-medium text-blue-700">
            Connected GSRTC Route planner
          </p>

          <h2 className="mt-6 text-2xl font-semibold text-slate-900">
            Find a route for non-direct connections.
          </h2>

          <p className="mx-auto mt-3 max-w-3xl text-slate-600">
            BusSetu checks direct services, long-route boarding segments and
            safe one-stop connections.
          </p>
        </header>

        <section className="rounded-3xl bg-white/90 p-6 shadow-xl ring-1 ring-blue-100 backdrop-blur">
          <form onSubmit={handleSearch} className="grid gap-5 md:grid-cols-4">
            <div className="relative">
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                From
              </label>
              <input
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                placeholder="Select origin"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              />
              {fromSuggestions.length > 0 && (
                <div className="absolute z-20 mt-2 max-h-56 w-full overflow-auto rounded-xl border border-slate-200 bg-white shadow-lg">
                  {fromSuggestions.map((stop) => (
                    <button
                      type="button"
                      key={stop}
                      onClick={() => setFrom(stop)}
                      className="block w-full px-4 py-2 text-left text-sm hover:bg-blue-50"
                    >
                      {stop}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className="relative">
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                To
              </label>
              <input
                value={to}
                onChange={(e) => setTo(e.target.value)}
                placeholder="Select destination"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              />
              {toSuggestions.length > 0 && (
                <div className="absolute z-20 mt-2 max-h-56 w-full overflow-auto rounded-xl border border-slate-200 bg-white shadow-lg">
                  {toSuggestions.map((stop) => (
                    <button
                      type="button"
                      key={stop}
                      onClick={() => setTo(stop)}
                      className="block w-full px-4 py-2 text-left text-sm hover:bg-blue-50"
                    >
                      {stop}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Date
              </label>
              <input
                type="date"
                value={date}
                min={todayISO()}
                max={maxDateISO()}
                onChange={(e) => setDate(e.target.value)}
                className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              />
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={loadingStops || loadingSearch}
                className="w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white shadow-md transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
              >
                {loadingSearch ? "Searching..." : "Find Routes"}
              </button>
            </div>
          </form>

          {loadingStops && (
            <p className="mt-4 text-sm text-slate-500">Loading stations...</p>
          )}

          {error && (
            <p className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
              {error}
            </p>
          )}
        </section>

        {results && (
          <section className="mt-8">
            <div className="mb-4">
              <h3 className="text-xl font-bold text-slate-900">
                {results.source} → {results.destination}
              </h3>
              <p className="text-sm text-slate-600">{results.message}</p>
            </div>

            {allRoutes.length === 0 ? (
              <div className="rounded-2xl bg-white p-6 shadow ring-1 ring-slate-100">
                <p className="font-medium text-slate-700">
                  No routes found for this connection.
                </p>
              </div>
            ) : (
              <div className="grid gap-5">
                {allRoutes.map((route, index) => (
                  <div
                    key={index}
                    className="rounded-2xl bg-white p-6 shadow-lg ring-1 ring-blue-100"
                  >
                    <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <h4 className="text-lg font-bold text-blue-950">
                          Option {index + 1}
                          {route.transfer ? ` via ${route.transfer}` : ""}
                        </h4>
                        <p className="text-sm text-slate-600">
                          Total: {minutesToText(route.total_duration_minutes)} ·
                          Fare: ₹{route.estimated_fare}
                          {route.waiting_minutes !== undefined
                            ? ` · Wait: ${minutesToText(route.waiting_minutes)}`
                            : ""}
                        </p>
                      </div>

                      {route.risk && (
                        <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700">
                          {route.risk} risk
                        </span>
                      )}
                    </div>

                    <div className="space-y-3">
                      {route.legs.map((leg, legIndex) => (
                        <div
                          key={legIndex}
                          className="rounded-xl border border-slate-200 bg-slate-50 p-4"
                        >
                          <div className="flex flex-wrap justify-between gap-2">
                            <div>
                              <p className="font-semibold text-slate-900">
                                {leg.from} → {leg.to}
                              </p>
                              <p className="text-sm text-slate-600">
                                {leg.service_name}
                              </p>
                            </div>

                            <div className="text-right">
                              <p className="font-semibold text-slate-900">
                                {leg.departure} → {leg.arrival}
                              </p>
                              <p className="text-sm text-slate-600">
                                {leg.bus_type} · ₹{leg.fare}
                              </p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}