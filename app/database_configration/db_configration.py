from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")


async def connect_to_mongo():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    return client.get_database()


async def disconnect_to_mongo():
    client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    return client.close()
