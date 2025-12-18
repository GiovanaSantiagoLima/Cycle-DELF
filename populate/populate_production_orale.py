from datetime import datetime
from app.database import materials_collection

materials = [
    {
        "competence": "Production Orale",
        "level": "B1",
        "type": "prompt",
        "content": "Parlez de votre routine quotidienne pendant 2 minutes.",
        "created_at": datetime.now()
    },
    {
        "competence": "Production Orale",
        "level": "B1",
        "type": "prompt",
        "content": "Décrivez une personne importante dans votre vie.",
        "created_at": datetime.now()
    }
]

materials_collection.insert_many(materials)