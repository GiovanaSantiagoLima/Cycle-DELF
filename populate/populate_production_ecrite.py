from datetime import datetime
from app.database import materials_collection

materials = [
    {
        "competence": "Production Écrite",
        "level": "B1",
        "type": "prompt",
        "content": "Écrivez un email pour demander des informations sur un cours.",
        "created_at": datetime.now()
    },
    {
        "competence": "Production Écrite",
        "level": "B1",
        "type": "prompt",
        "content": "Rédigez un texte sur vos projets futurs.",
        "created_at": datetime.now()
    }
]

materials_collection.insert_many(materials)
