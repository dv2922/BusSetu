from pydantic import BaseModel, Field
from typing import List, Optional


class Leg(BaseModel):
    from_stop: str = Field(..., alias="from")
    to_stop: str = Field(..., alias="to")
    departure: str
    arrival: str
    bus_type: str
    fare: int
    service_name: str

    class Config:
        populate_by_name = True


class ConnectedRoute(BaseModel):
    transfer: str
    total_duration_minutes: int
    waiting_minutes: int
    risk: str
    score: float
    estimated_fare: int
    legs: List[Leg]


class SearchResponse(BaseModel):
    source: str
    destination: str
    date: str
    direct_routes: List[Leg]
    connected_routes: List[ConnectedRoute]
    message: Optional[str] = None
