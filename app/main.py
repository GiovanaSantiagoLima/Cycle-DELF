from fastapi import FastAPI, HTTPException
from datetime import datetime
from bson import ObjectId
from app.database import users_collection, sessions_collection
from app.funcionalidade import (
    start_session,
    finish_session,
    get_cycle_status
)

app = FastAPI()

# -----------------------------
# USERS
# -----------------------------

@app.post("/users")
def create_user(user: dict):
    # Garante que level padrão existe se não for enviado
    if "level" not in user:
        user["level"] = "A1"
        
    user["created_at"] = datetime.now()
    result = users_collection.insert_one(user)
    
    return {
        "message": "Usuário criado com sucesso",
        "id": str(result.inserted_id)
    }

@app.get("/users")
def list_users():
    users = []
    # Converte o ObjectId do Mongo para string para não dar erro no retorno
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

# -----------------------------
# SESSIONS / CICLO
# -----------------------------

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

@app.get("/cycle/{user_id}")
def get_user_cycle(user_id: str):
    try:
        return get_cycle_status(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))