"""Search request/response schemas."""

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    radius_meters: int = 5000
    source: str = "google_places"


class SearchResult(BaseModel):
    google_place_id: str | None = None
    business_name: str
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    category: str | None = None
    rating: float | None = None
    review_count: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    source: str = "google_places"
    already_saved: bool = False


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    query: str
    cached: bool = False
