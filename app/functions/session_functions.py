from datetime import datetime
from bson import ObjectId
from app.database import sessions_collection

# CREATE SESSION
def create_session(user_id: str):
    session = {
        "user_id": ObjectId(user_id),
        "duration_minutes": 15,
        "created_at": datetime.now(),
        "completed": True
    }

    sessions_collection.insert_one(session)

    total_sessions = sessions_collection.count_documents({
        "user_id": ObjectId(user_id)
    })

    return {
        "message": "Sessão criada com sucesso",
        "total_sessions": total_sessions,
        "cycle_completed": total_sessions >= 4
    }


# READ SESSIONS (por usuário)
def get_sessions(user_id: str):
    sessions = list(
        sessions_collection.find(
            {"user_id": ObjectId(user_id)},
            {"_id": 0}
        )
    )
    return sessions


# UPDATE SESSION
def update_session(session_id: str, data: dict):
    result = sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": data}
    )

    if result.modified_count == 1:
        return {"message": "Sessão atualizada com sucesso"}
    
    return {"message": "Nenhuma sessão foi atualizada"}


# DELETE SESSION
def delete_session(session_id: str):
    result = sessions_collection.delete_one(
        {"_id": ObjectId(session_id)}
    )

    if result.deleted_count == 1:
        return {"message": "Sessão deletada com sucesso"}

    return {"message": "Sessão não encontrada"}
