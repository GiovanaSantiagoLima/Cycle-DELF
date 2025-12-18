from datetime import datetime
from app.database import users_collection

users = [
    {
        "name": "Giovana",
        "level": "B1",
        "created_at": datetime.now()
    },
    {
        "name": "Ana",
        "level": "B2",
        "created_at": datetime.now()
    },
    {
        "name": "Lucas",
        "level": "A2",
        "created_at": datetime.now()
    }
]

users_collection.insert_many(users)

