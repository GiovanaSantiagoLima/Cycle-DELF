from datetime import datetime, timedelta, date
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
    # CORREÇÃO: Convertendo date para datetime para o MongoDB aceitar
    today_date = date.today()
    today_datetime = datetime.combine(today_date, datetime.min.time())

    today_sessions = list(
        sessions_collection.find({
            "user_id": user_id,
            "date": today_datetime  # Usando a data convertida
        })
    )

    completed_competencies = [
        s["competency"] for s in today_sessions if s.get("completed")
    ]

    if len(completed_competencies) >= MAX_SESSIONS:
        return {
            "message": "Ciclo diário concluído",
            "completed_competencies": completed_competencies,
            "cycle_completed": True
        }

    next_competency = None
    for comp in COMPETENCIES:
        if comp not in completed_competencies:
            next_competency = comp
            break

    session = {
        "user_id": user_id,
        "competency": next_competency,
        "date": today_datetime, # Salva como datetime
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=SESSION_DURATION),
        "completed": False
    }

    result = sessions_collection.insert_one(session)

    return {
        "message": "Sessão iniciada com sucesso",
        "session_id": str(result.inserted_id),
        "competency": next_competency,
        "ends_at": session["end_time"],
        "completed_competencies": completed_competencies,
        "cycle_completed": False
    }


def finish_session(session_id: str):
    session = sessions_collection.find_one({"_id": ObjectId(session_id)})

    if not session:
        return {"message": "Sessão não encontrada"}

    if session.get("completed"):
        return {
            "message": "Sessão já finalizada",
            "competency": session["competency"]
        }

    sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"completed": True, "finished_at": datetime.now()}}
    )

    # CORREÇÃO: Convertendo date para datetime para o MongoDB aceitar
    today_date = date.today()
    today_datetime = datetime.combine(today_date, datetime.min.time())

    completed_sessions = list(
        sessions_collection.find({
            "user_id": session["user_id"],
            "date": today_datetime,
            "completed": True
        })
    )

    completed_competencies = [s["competency"] for s in completed_sessions]

    next_competency = None
    for comp in COMPETENCIES:
        if comp not in completed_competencies:
            next_competency = comp
            break

    return {
        "message": "Sessão finalizada com sucesso",
        "completed_competency": session["competency"],
        "completed_competencies": completed_competencies,
        "next_competency": next_competency,
        "cycle_completed": len(completed_competencies) == MAX_SESSIONS
    }


def get_cycle_status(user_id: str):
    # CORREÇÃO: Convertendo date para datetime para o MongoDB aceitar
    today_date = date.today()
    today_datetime = datetime.combine(today_date, datetime.min.time())

    sessions = list(
        sessions_collection.find({
            "user_id": user_id,
            "date": today_datetime,
            "completed": True
        }, {"_id": 0})
    )

    completed_competencies = [s["competency"] for s in sessions]

    next_competency = None
    for comp in COMPETENCIES:
        if comp not in completed_competencies:
            next_competency = comp
            break

    return {
        "user_id": user_id,
        "completed_sessions": len(completed_competencies),
        "completed_competencies": completed_competencies,
        "next_competency": next_competency,
        "cycle_completed": len(completed_competencies) == MAX_SESSIONS
    }