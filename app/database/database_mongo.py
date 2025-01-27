from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE]