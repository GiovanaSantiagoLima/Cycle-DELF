from datetime import datetime
from app.database import materials_collection, questions_collection

materials = [
    {
        "competence": "Compréhension Orale",
        "level": "B1",
        "type": "audio",
        "title": "La routine quotidienne d’un étudiant",
        "audio_url": "https://www.youtube.com/watch?v=VIDEO_1",
        "description": "Un étudiant parle de sa routine quotidienne.",
        "created_at": datetime.now()
    },
    {
        "competence": "Compréhension Orale",
        "level": "B1",
        "type": "audio",
        "title": "Travailler et étudier en même temps",
        "audio_url": "https://www.youtube.com/watch?v=VIDEO_2",
        "description": "Une personne explique comment elle concilie travail et études.",
        "created_at": datetime.now()
    },
    {
        "competence": "Compréhension Orale",
        "level": "B1",
        "type": "audio",
        "title": "Les loisirs pendant la semaine",
        "audio_url": "https://www.youtube.com/watch?v=VIDEO_3",
        "description": "Une discussion sur les loisirs et le temps libre.",
        "created_at": datetime.now()
    }
]

for material in materials:
    material_id = materials_collection.insert_one(material).inserted_id

    if material["title"] == "La routine quotidienne d’un étudiant":
        questions = [
            {
                "material_id": str(material_id),
                "question": "De quoi parle la vidéo ?",
                "options": [
                    "La routine quotidienne",
                    "Les vacances",
                    "La famille",
                    "Le sport"
                ],
                "correct_answer": "La routine quotidienne",
                "created_at": datetime.now()
            },
            {
                "material_id": str(material_id),
                "question": "Qui parle dans la vidéo ?",
                "options": [
                    "Un étudiant",
                    "Un professeur",
                    "Un journaliste",
                    "Un médecin"
                ],
                "correct_answer": "Un étudiant",
                "created_at": datetime.now()
            }
        ]

    elif material["title"] == "Travailler et étudier en même temps":
        questions = [
            {
                "material_id": str(material_id),
                "question": "Quel est le sujet principal de la vidéo ?",
                "options": [
                    "Le travail et les études",
                    "Les loisirs",
                    "Les voyages",
                    "La santé"
                ],
                "correct_answer": "Le travail et les études",
                "created_at": datetime.now()
            },
            {
                "material_id": str(material_id),
                "question": "Pourquoi la personne travaille-t-elle ?",
                "options": [
                    "Pour gagner de l’expérience",
                    "Pour voyager",
                    "Pour faire du sport",
                    "Pour apprendre une langue"
                ],
                "correct_answer": "Pour gagner de l’expérience",
                "created_at": datetime.now()
            }
        ]

    else:
        questions = [
            {
                "material_id": str(material_id),
                "question": "Quand la personne parle-t-elle de ses loisirs ?",
                "options": [
                    "Pendant la semaine",
                    "Le matin",
                    "Pendant les vacances",
                    "La nuit"
                ],
                "correct_answer": "Pendant la semaine",
                "created_at": datetime.now()
            },
            {
                "material_id": str(material_id),
                "question": "Quel est le thème principal ?",
                "options": [
                    "Le temps libre",
                    "Le travail",
                    "Les études",
                    "La famille"
                ],
                "correct_answer": "Le temps libre",
                "created_at": datetime.now()
            }
        ]

    questions_collection.insert_many(questions)

