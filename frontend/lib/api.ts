const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function getStops() {
  const res = await fetch(`${API_BASE_URL}/api/stops`);
  if (!res.ok) throw new Error("Failed to fetch stops");
  return res.json();
}

export async function searchRoutes(from: string, to: string, date: string) {
  const params = new URLSearchParams({ from, to, date });
  const res = await fetch(`${API_BASE_URL}/api/search?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to search routes");
  return res.json();
}