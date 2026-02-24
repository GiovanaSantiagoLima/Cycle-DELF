from pymongo import MongoClient

MONGO_URI = "mongodb+srv://admin:DELF2026@cluster0.k9ycyvh.mongodb.net/cycledelf?retryWrites=true&w=majority"


client = MongoClient(MONGO_URI)

db = client["cycledelf"]

users_collection = db["users"]
sessions_collection = db["sessions"]
materials_collection = db["materials"]
questions_collection = db["questions"]

from pymongo import ASCENDING, TEXT, GEOSPHERE
import os

def create_db_indexes():
    """Cria os índices necessários para performance e buscas avançadas"""
    try:
        users_collection.create_index([("name", ASCENDING)], unique=True)
        materials_collection.create_index([("content", TEXT)])        
        users_collection.create_index([("location", GEOSPHERE)])
        
        print("✅ Índices criados/verificados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar índices: {e}")

create_db_indexes()