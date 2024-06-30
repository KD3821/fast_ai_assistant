from typing import List

from langchain_core.tools import tool

from src.data.mongodb import travel
from src.schemas.travel import ItineraryVector, Ship

__all__ = ["tools"]


@tool
def details_lookup(query: str) -> str:
    """find cruise duration in days, departing-from-port, arriving-to-port, cabin prices, destinations by cruise"""
    itineraries: List[ItineraryVector] = travel.details_search(query)
    content = ""

    for it in itineraries:
        content += (
            f"Cruise name: {it.name}\nDuration: {it.duration}\nShip: {it.ship_name}\n"
            f"Departure from: {it.port}\nDestinations: {it.destinations}\nPrices: {it.cabins}\n\n"
        )

    return content


@tool
def vacation_lookup(query: str) -> str:
    """find information on vacations and trips"""
    ships: List[Ship] = travel.similarity_search(query)
    content = ""

    for ship in ships:
        content += f"Cruise ship: {ship.name}\nDescription: {ship.description}\nAmenities:\n-{ship.amenities}\n\n"

    return content


@tool
def itinerary_lookup(ship_name: str) -> str:
    """find ship itinerary, cruise packages and destinations by ship name"""
    it = travel.itinerary_search(ship_name)
    results = ""

    for i in it:
        results += f" Cruise Package {i.name} room prices: {'/n-'.join(i.rooms)} schedule: {'/n-'.join(i.schedule)}"

    return results


@tool
def book_cruise(package_name: str, passenger_name: str, room: str) -> str:
    """book cruise using package name and passenger name and room"""
    print(f"Package: {package_name} passenger: {passenger_name} room: {room}")

    # LLM defaults empty name to John Doe
    if passenger_name == "John Doe":
        return "In order to book a cruise I will need to know your name."
    else:
        if room == "":
            return "which room would you like to book"
        return "Cruise has been booked, ref number is 343242"


tools = [details_lookup, vacation_lookup, itinerary_lookup, book_cruise]
