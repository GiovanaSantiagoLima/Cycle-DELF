from datetime import datetime, timedelta, date
from app.database import db_connection
from bson import ObjectId

# Configurações de Ciclo
MAX_SESSIONS = 4
SESSION_DURATION = 15  # minutos

COMPETENCIES = [
    "Compréhension Orale",
    "Production Écrite",
    "Compréhension Écrite",
    "Production Orale"
]

async def start_session(user_id: str):
    """Inicia uma nova sessão de estudo assincronamente."""
    today_date = date.today()
    today_datetime = datetime.combine(today_date, datetime.min.time())

    # No Motor (MongoDB Assíncrono), usamos to_list para pegar os resultados
    cursor = db_connection.sessions.find({
        "user_id": user_id,
        "date": today_datetime
    })
    today_sessions = await cursor.to_list(length=100)

    completed_competencies = [
        s["competency"] for s in today_sessions if s.get("completed")
    ]

    if len(completed_competencies) >= MAX_SESSIONS:
        return {
            "message": "Ciclo diário concluído",
            "completed_competencies": completed_competencies,
            "cycle_completed": True
        }

    # Encontra a próxima competência disponível
    next_competency = next((comp for comp in COMPETENCIES if comp not in completed_competencies), None)

    session = {
        "user_id": user_id,
        "competency": next_competency,
        "date": today_datetime,
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=SESSION_DURATION),
        "completed": False
    }

    result = await db_connection.sessions.insert_one(session)

    return {
        "message": "Sessão iniciada com sucesso",
        "session_id": str(result.inserted_id),
        "competency": next_competency,
        "ends_at": session["end_time"],
        "completed_competencies": completed_competencies,
        "cycle_completed": False
    }


async def finish_session(session_id: str):
    """Finaliza uma sessão existente assincronamente."""
    session = await db_connection.sessions.find_one({"_id": ObjectId(session_id)})

    if not session:
        return {"message": "Sessão não encontrada"}

    if session.get("completed"):
        return {
            "message": "Sessão já finalizada",
            "competency": session["competency"]
        }

    # Atualiza o status para completado
    await db_connection.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"completed": True, "finished_at": datetime.now()}}
    )

    today_datetime = datetime.combine(date.today(), datetime.min.time())

    # Busca sessões completadas hoje para calcular o progresso
    cursor = db_connection.sessions.find({
        "user_id": session["user_id"],
        "date": today_datetime,
        "completed": True
    })
    completed_sessions = await cursor.to_list(length=100)

    completed_competencies = [s["competency"] for s in completed_sessions]
    next_competency = next((comp for comp in COMPETENCIES if comp not in completed_competencies), None)

    return {
        "message": "Sessão finalizada com sucesso",
        "completed_competency": session["competency"],
        "completed_competencies": completed_competencies,
        "next_competency": next_competency,
        "cycle_completed": len(completed_competencies) == MAX_SESSIONS
    }


async def get_cycle_status(user_id: str):
    """Verifica o status atual do ciclo do usuário assincronamente."""
    today_datetime = datetime.combine(date.today(), datetime.min.time())

    cursor = db_connection.sessions.find({
        "user_id": user_id,
        "date": today_datetime,
        "completed": True
    }, {"_id": 0})
    
    sessions = await cursor.to_list(length=100)

    completed_competencies = [s["competency"] for s in sessions]
    next_competency = next((comp for comp in COMPETENCIES if comp not in completed_competencies), None)

    return {
        "user_id": user_id,
        "completed_sessions": len(completed_competencies),
        "completed_competencies": completed_competencies,
        "next_competency": next_competency,
        "cycle_completed": len(completed_competencies) == MAX_SESSIONS
    }