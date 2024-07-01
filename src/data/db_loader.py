from typing import List

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from src.database import async_client, sync_client
from src.settings import fast_ai_settings


class DBLoader:
    def __init__(self, db_name):
        self.async_db = async_client[db_name]
        self.sync_db = sync_client[db_name]

    async def _collection_exists(self, collection_name: str) -> bool:
        collections = await self.async_db.list_collection_names()
        if collection_name not in collections:
            return False
        return True

    async def _drop_collection(self, collection_name: str) -> None:
        collection_exist = await self._collection_exists(collection_name)
        if collection_exist:
            await self.async_db.drop_collection(collection_name)

    async def upload_data(self, data: list, collection_name: str) -> None:
        print(f"--load {collection_name}--")
        await self._drop_collection(collection_name)
        collection = self.async_db[collection_name]
        await collection.insert_many(data)

    async def load_vectors(self, data: list, collection_name: str):
        print(f"--load vectors {collection_name}--")
        docs = None
        if collection_name == "ships":
            docs = await self.load_ships(data)
        elif collection_name == "destinations":
            docs = await self.load_destinations(data)
        elif collection_name == "itineraries":
            docs = await self.load_itineraries(data)
        if docs is not None:
            documents = await self.split_docs(docs)
            Chroma.from_documents(
                documents,
                OpenAIEmbeddings(
                    openai_api_key=fast_ai_settings.openai_api_key,
                    model=fast_ai_settings.embedding_model,
                ),
                persist_directory=str(fast_ai_settings.vectorstore_dir),
            )
        collection = self.sync_db[collection_name]
        return collection

    @staticmethod
    async def load_ships(data: list) -> List[Document]:
        docs: List[Document] = list()

        for obj in data:
            name = obj.get("name")
            text = f"{obj.get('description')} {' '.join(obj.get('amenities'))}"
            description = obj.get("description")
            amenities = obj.get("amenities")

            metadata = {
                "ship_id": obj.get("ship_id"),
                "name": name,
                "description": description,
                "amenities": "\n-".join(amenities),
            }

            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    @staticmethod
    async def load_destinations(data: list) -> List[Document]:
        docs: List[Document] = list()

        for obj in data:
            name = obj.get("name")
            text = f"{obj.get('description')} {' '.join(obj.get('activities'))}"
            location = obj.get("location")
            description = obj.get("description")
            activities = obj.get("activities")

            metadata = {
                "destination_id": obj.get("destination_id"),
                "name": name,
                "location": location,
                "description": description,
                "activities": "\n".join(activities),
            }

            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    @staticmethod
    async def load_itineraries(data: list) -> List[Document]:
        docs: List[Document] = list()

        for obj in data:
            name = obj.get("name")[6:]
            duration = obj.get("name")[:5]
            ship_id = obj.get("ship").get("ship_id")
            ship_name = obj.get("ship").get("name")
            route = obj.get("itinerary")
            prices = obj.get("prices")
            port = None
            destinations = set()
            for point in route:
                if point.get("type") == "port":
                    port = point.get("location")
                elif point.get("type") == "destination":
                    destinations.add(point.get("location"))

            d_list = list(destinations)

            price_list = list()
            for price in prices:
                price_list.append((float(price.get("price")), price.get("name")))
            price_list.sort()

            cabins = ", ".join(
                [f"${cost} for {cabin_name} cabin" for cost, cabin_name in price_list]
            )

            text = (
                f"{name} is a {duration} cruise on board of '{ship_name}' ship, "
                f"departing-arriving port is {port},"
                f"lowest price is ${price_list[0][0]} for {price_list[0][1]} type of cabin,"
                f"highest price is ${price_list[-1][0]} for {price_list[-1][1]} type of cabin,"
                f"visiting destinations: {', '.join(d_list)}"
            )

            metadata = {
                "name": name,
                "duration": duration,
                "ship_id": ship_id,
                "ship_name": ship_name,
                "port": port,
                "destinations": ", ".join(d_list),
                "cabins": cabins,
            }

            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    @staticmethod
    async def split_docs(docs: List[Document]):
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=200, chunk_overlap=40
        )
        documents = text_splitter.split_documents(docs)
        return documents

