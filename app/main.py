import uvicorn
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import List 
from pydantic import BaseModel 
from app.utils.config import settings
from app.routers import books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)

async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
       settings.MONGO_URI)
    app.mongodb = app.mongodb_client.get_database(settings.DATABASE)
    print("MongoDB connected.")

async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")

app = FastAPI(lifespan=lifespan)
app.include_router(books_router.router)

