from fastapi import FastAPI, HTTPException
from datetime import datetime
from bson import ObjectId
from app.database import users_collection, sessions_collection, materials_collection
from app.funcionalidade import (
    start_session,
    finish_session,
    get_cycle_status
)
from pymongo import MongoClient, ASCENDING, TEXT, GEOSPHERE 
from typing import Optional 
import uvicorn
import random 

app = FastAPI()
# ---------------------------------------------------------
# ROTAS DE USUÁRIOS
# ---------------------------------------------------------

@app.post("/users")
def create_user(user: dict):
    if "level" not in user:
        user["level"] = "A1"
    if "location" not in user:
        user["location"] = {
            "type": "Point",
            "coordinates": [
                random.uniform(-46.8, -46.3), # Longitude
                random.uniform(-23.7, -23.4)  # Latitude
            ]
        }
    
    user["created_at"] = datetime.now()
    result = users_collection.insert_one(user)
    return {"message": "Usuário criado", "id": str(result.inserted_id)}

@app.get("/users")
def list_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.get("/users/filter")
async def filter_users(level: Optional[str] = None):
    query = {}
    if level:
        query["level"] = level.strip()
    
    # Busca correta na coleção de usuários
    users = list(users_collection.find(query))
    for u in users:
        u["_id"] = str(u["_id"])
    return users

@app.post("/users/populate-locations")
async def populate_locations():
    # Busca apenas quem não tem o campo 'location'
    users_sem_loc = users_collection.find({"location": {"$exists": False}})
    updated_count = 0

    for user in users_sem_loc:
        random_lon = random.uniform(-46.8, -46.3)
        random_lat = random.uniform(-23.7, -23.4)

        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "location": {
                        "type": "Point",
                        "coordinates": [random_lon, random_lat] # Longitude primeiro
                    }
                }
            }
        )
        updated_count += 1

    return {"status": "success", "message": f"{updated_count} usuários atualizados!"}


@app.get("/users/nearby")
async def get_nearby_users(lat: float, lon: float, radius_km: float = 10):
    query = {
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": radius_km * 1000
            }
        }
    }
    users = list(users_collection.find(query))
    for u in users:
        u["_id"] = str(u["_id"])
    return users



# ---------------------------------------------------------
# ROTAS DE MATERIAIS
# ---------------------------------------------------------

@app.get("/materials/search")
async def search_materials(q: str):
    clean_q = q.strip()
    query = {"$text": {"$search": clean_q}}
    
    materials = list(materials_collection.find(query))
    for m in materials:
        m["_id"] = str(m["_id"])
    return materials

# ---------------------------------------------------------
# SESSIONS E CICLO
# ---------------------------------------------------------

@app.post("/sessions/start/{user_id}")
def start_user_session(user_id: str):
    try:
        return start_session(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sessions/finish/{session_id}")
def finish_user_session(session_id: str):
    try:
        return finish_session(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Sessão inválida")
# -----------------------------
# REQUISITOS NO SQL: POPULATE 
# -----------------------------

@app.post("/populate")
async def populate_api(count: int = 50):
    try:
        from populate.seed import generate_bulk_data
        generate_bulk_data(n_materials=count)
        return {"status": "success", "message": f"{count} registros inseridos via insertMany"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao popular: {str(e)}")

# -----------------------------
# DATA ANALYTICS: AGGREGATION PIPELINES
# -----------------------------

@app.get("/analytics/activity-by-competence/{user_id}")
def activity_by_competence(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$competence",
                "sessions": {"$sum": 1},
                "avg_score": {"$avg": "$score"}
            }
        },
        {"$sort": {"sessions": -1}}
    ]

    return list(sessions_collection.aggregate(pipeline))
from bson import ObjectId

@app.get("/analytics/monthly-progress/{user_id}")
def monthly_progress(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$start_time"},
                    "month": {"$month": "$start_time"}
                },
                "sessions": {"$sum": 1},
                "avg_score": {"$avg": "$score"}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]

    return list(sessions_collection.aggregate(pipeline))


@app.get("/analytics/top-users")
def top_users():
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "total_sessions": {"$sum": 1}
            }
        },
        {"$sort": {"total_sessions": -1}},
        {"$limit": 10}
    ]

    return list(sessions_collection.aggregate(pipeline))

# -----------------------------
# INDICES 
# -----------------------------

def criando_index():
        users_collection.create_index([("name", ASCENDING)], unique=True)
        users_collection.create_index([("level", ASCENDING)])
        users_collection.create_index([("location", GEOSPHERE)])
        
        materials_collection.create_index([
            ("title", TEXT), 
            ("content", TEXT),
            ("competence", TEXT)
        ], name="busca_texto_global")
        
        print("✅ índices configurados!")
criando_index()


@app.get("/users/filter")
async def filter_users(level: Optional[str] = None):
    query = {}
    if level:
        query["level"] = level.strip()
    
    users = list(users_collection.find(query))
    # Converte ObjectId para string
    for u in users:
        u["_id"] = str(u["_id"])
    return users

import random


