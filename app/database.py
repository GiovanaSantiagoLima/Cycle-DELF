import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

MONGO_URI = "mongodb+srv://admin:DELF2026@cluster0.k9ycyvh.mongodb.net/cycledelf?retryWrites=true&w=majority"
REDIS_URL = "redis://default:WbxSx1aucKYkxbfJwSBfMxfwbIiSWW37@redis-15626.c261.us-east-1-4.ec2.cloud.redislabs.com:15626"

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