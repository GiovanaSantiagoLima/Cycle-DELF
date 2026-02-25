from pymongo import MongoClient
from contextlib import asynccontextmanager
import os
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega as URLs das variáveis de ambiente
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")

class Database:
    client: AsyncIOMotorClient = None
    db = None
    redis = None
    
    users = None
    sessions = None
    materials = None
    questions = None

db_connection = Database()

async def connect_to_nosql():
    db_connection.client = AsyncIOMotorClient(MONGO_URI)
    db_connection.db = db_connection.client["cycledelf"]
    
    db_connection.users = db_connection.db["users"]
    db_connection.sessions = db_connection.db["sessions"]
    db_connection.materials = db_connection.db["materials"]
    db_connection.questions = db_connection.db["questions"]

    db_connection.redis = redis.from_url(REDIS_URL, decode_responses=True)
    
    print("✅ Conectado ao MongoDB Atlas e ao Redis!")

async def close_nosql_connections():
    db_connection.client.close()
    await db_connection.redis.close()