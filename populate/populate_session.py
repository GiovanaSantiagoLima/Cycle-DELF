from datetime import datetime, timedelta
from app.database import sessions_collection

# user_id real copiado do MongoDB Atlas
USER_ID = "694065c87b0db345899ff709"

sessions = [
    {
        "user_id": USER_ID,
        "competence": "Compréhension Orale",
        "session_number": 1,
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=15),
        "completed": True
    },
    {
        "user_id": USER_ID,
        "competence": "Production Écrite",
        "session_number": 2,
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=15),
        "completed": True
    }
]

sessions_collection.insert_many(sessions)

print("✅ Sessões inseridas com sucesso!")
