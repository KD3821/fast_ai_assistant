import os

import pymongo
from motor import motor_asyncio
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv('DB_HOST')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
VECTORSTORE_DIR = os.getenv('VECTORSTORE_DIR')

embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=EMBEDDING_MODEL)

MONGO_URL = f"mongodb://{DB_HOST}:27017"

sync_client = pymongo.MongoClient(MONGO_URL)

async_client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)

vector_store = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embedding)
