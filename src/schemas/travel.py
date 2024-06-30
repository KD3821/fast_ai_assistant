from typing import List

from pydantic import BaseModel


class Ship(BaseModel):
    name: str
    description: str
    amenities: str


class Room(BaseModel):
    name: str
    price: str


class Itinerary(BaseModel):
    ship_id: str
    name: str
    rooms: List[str]
    schedule: List[str]


class ItineraryVector(BaseModel):
    name: str
    duration: str
    ship_id: str | None
    ship_name: str
    port: str
    destinations: str
    cabins: str
