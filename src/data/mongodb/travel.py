import locale
from typing import List

from langchain.docstore.document import Document

from src.database import embedding, sync_client, vector_store
from src.schemas.travel import Itinerary, ItineraryVector, Ship
from src.settings import fast_ai_settings


def results_to_itinerary(result: Document) -> ItineraryVector:
    return ItineraryVector(
        name=result.metadata.get("name"),
        duration=result.metadata.get("duration"),
        ship_id=result.metadata.get("ship_id"),
        ship_name=result.metadata.get("ship_name"),
        port=result.metadata.get("port"),
        destinations=result.metadata.get("destinations"),
        cabins=result.metadata.get("cabins"),
    )


def results_to_ship(result: Document) -> Ship:
    return Ship(
        name=result.metadata.get("name"),
        description=result.metadata.get("description"),
        amenities=result.metadata.get("amenities"),
    )


def get_ship_by_name(name: str) -> str:
    db = sync_client[fast_ai_settings.db_name]
    collection = db["ships"]
    print(f"-{name}-")
    ship = collection.find_one({"name": name.strip()})
    if ship is None:
        return ""
    if "ship_id" in ship:
        return ship.get("ship_id")
    else:
        print("ship not found")
        return ""


def itinerary_search(name: str) -> List[Itinerary]:
    data = list()
    db = sync_client[fast_ai_settings.db_name]
    collection = db["itinerary"]
    ship_id = get_ship_by_name(name)
    if ship_id != "":
        cursor = collection.find({"ship.ship_id": ship_id})
        locale.setlocale(locale.LC_ALL, "")
        for item in cursor:
            data.append(
                Itinerary(
                    ship_id=item.get("ship").get("ship_id"),
                    name=item.get("name"),
                    rooms=[
                        f" room {p.get('name')} price {locale.currency(p.get('price'))} "
                        for p in item.get("prices")
                    ],
                    schedule=[
                        f" day {i.get('Day')} {i.get('type')} location {i.get('location')} "
                        for i in item.get("itinerary")
                    ],
                )
            )
    return data


def similarity_search(query: str) -> List[Ship]:

    docs = vector_store.similarity_search_with_score(
        query,
        k=2,
        where_document={"$or": [{"$contains": "ship_id"}, {"$contains": "amenities"}]},
    )

    # Cosine Similarity:
    # It measures the cosine of the angle between two vectors in an n-dimensional space.
    # The values of similarity metrics typically range between 0 and 1, with higher values indicating greater similarity
    # between the vectors.
    docs_filters = [doc for doc, score in docs if score >= 0.78]

    # List the scores for documents
    for doc, score in docs:
        print(f"{score=}")

    # Print number of documents passing score threshold
    print(f"total docs: {len(docs_filters)}")

    return [results_to_ship(document) for document in docs_filters]


def details_search(query: str) -> List[Itinerary]:

    docs = vector_store.similarity_search_with_score(
        query,
        k=3,
        where_document={
            "$or": [
                {"$contains": "visiting destinations"},
                {"$contains": "departing-arriving port is"},
                {"$contains": "lowest price is"},
                {"$contains": "highest price is"},
            ]
        },
    )
    docs_filters = [doc for doc, score in docs if score >= 0.78]

    # List the scores for documents
    for doc, score in docs:
        print(f"{score=}")

    # Print number of documents passing score threshold
    print(f"total docs: {len(docs_filters)}")

    return [results_to_itinerary(document) for document in docs_filters]
