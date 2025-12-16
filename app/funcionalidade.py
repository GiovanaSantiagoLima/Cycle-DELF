from datetime import datetime, timedelta
from app.database import sessions_collection
from bson import ObjectId

MAX_SESSIONS = 4
SESSION_DURATION = 15  # minutos

COMPETENCIES = [
    "Compréhension Orale",
    "Production Écrite",
    "Compréhension Écrite",
    "Production Orale"
]


def start_session(user_id: str):
    # Conta sessões concluídas do usuário
    total_sessions = sessions_collection.count_documents({
        "user_id": user_id,
        "completed": True
    })

    if total_sessions >= MAX_SESSIONS:
        return {
            "message": "Ciclo concluído. Você completou todas as competências do dia."
        }

    session_number = total_sessions + 1
    competency = COMPETENCIES[total_sessions]

    session = {
        "user_id": user_id,
        "session_number": session_number,
        "competency": competency,
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=SESSION_DURATION),
        "completed": False
    }

    sessions_collection.insert_one(session)

    return {
        "message": f"Sessão {session_number} iniciada",
        "competency": competency,
        "ends_at": session["end_time"]
    }

def get_cycle_status(user_id: str):
    sessions = list(
        sessions_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
    )

    completed_sessions = [s for s in sessions if s["completed"]]

    completed_competencies = [s["competency"] for s in completed_sessions]

    next_competency = None
    if len(completed_competencies) < MAX_SESSIONS:
        next_competency = COMPETENCIES[len(completed_competencies)]

    return {
        "user_id": user_id,
        "completed_sessions": len(completed_competencies),
        "completed_competencies": completed_competencies,
        "next_competency": next_competency,
        "cycle_completed": len(completed_competencies) == MAX_SESSIONS
    }


def finish_session(session_id: str):
    result = sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"completed": True, "finished_at": datetime.now()}}
    )

    if result.modified_count == 1:
        return {"message": "Sessão finalizada com sucesso"}

    return {"message": "Sessão não encontrada"}
