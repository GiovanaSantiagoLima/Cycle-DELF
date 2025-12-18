from datetime import datetime
from app.database import materials_collection, questions_collection

# ===== TEXTO 1 =====
material_1 = {
    "competence": "Compréhension Écrite",
    "level": "B1",
    "type": "text",
    "content": """Aujourd’hui, la technologie joue un rôle très important dans l’apprentissage des langues étrangères.
Grâce à Internet, les étudiants ont accès à une grande variété de ressources, comme des vidéos, des podcasts,
des applications mobiles et des plateformes interactives.

Beaucoup d’apprenants utilisent leur téléphone portable pour pratiquer le français chaque jour.
Par exemple, ils peuvent écouter des podcasts pendant les transports, lire des articles courts
ou écrire des messages dans des forums en ligne. Cela permet de pratiquer la langue de manière régulière,
même avec un emploi du temps chargé.

Cependant, la technologie ne remplace pas complètement l’interaction humaine.
Parler avec un professeur ou avec d’autres étudiants reste essentiel pour améliorer la prononciation
et la confiance à l’oral. L’idéal est donc de combiner les outils numériques avec des échanges réels.

En conclusion, la technologie facilite l’apprentissage du français, mais elle est plus efficace
lorsqu’elle est utilisée comme un complément et non comme la seule méthode d’étude.""",
    "created_at": datetime.now()
}

material_1_id = materials_collection.insert_one(material_1).inserted_id

questions_1 = [
    {
        "material_id": str(material_1_id),
        "question": "Quel est le thème principal du texte ?",
        "options": [
            "L’apprentissage des langues avec la technologie",
            "Le sport",
            "La santé",
            "La culture française"
        ],
        "correct_answer": "L’apprentissage des langues avec la technologie",
        "created_at": datetime.now()
    },
    {
        "material_id": str(material_1_id),
        "question": "Pourquoi la technologie est-elle utile pour les étudiants ?",
        "options": [
            "Elle permet d’étudier régulièrement malgré un emploi du temps chargé",
            "Elle remplace totalement les professeurs",
            "Elle empêche la concentration",
            "Elle réduit le temps d’étude"
        ],
        "correct_answer": "Elle permet d’étudier régulièrement malgré un emploi du temps chargé",
        "created_at": datetime.now()
    }
]

questions_collection.insert_many(questions_1)

# ===== TEXTO 2 =====
material_2 = {
    "competence": "Compréhension Écrite",
    "level": "B1",
    "type": "text",
    "content": """De nos jours, beaucoup d’étudiants ont des difficultés à organiser leur temps de travail.
Entre les études, le travail et la vie personnelle, il est parfois compliqué de rester motivé
et de garder une routine régulière.

Pour améliorer leurs résultats, certains étudiants décident de créer un planning d’étude.
Ils définissent des objectifs simples et réalisables, comme étudier quinze minutes par jour
ou réviser un thème spécifique chaque semaine. Cette méthode permet d’éviter le stress
et de progresser de manière plus efficace.

De plus, faire des pauses régulières est essentiel pour rester concentré.
Après une courte période de travail, une pause permet au cerveau de se reposer
et d’assimiler les informations plus facilement.

En conclusion, une bonne organisation du temps et des objectifs clairs sont des éléments clés
pour réussir ses études et maintenir une motivation constante.""",
    "created_at": datetime.now()
}

material_2_id = materials_collection.insert_one(material_2).inserted_id

questions_2 = [
    {
        "material_id": str(material_2_id),
        "question": "Quelle est la principale difficulté mentionnée dans le texte ?",
        "options": [
            "L’organisation du temps",
            "Le manque de professeurs",
            "La difficulté de la langue",
            "Le manque de technologie"
        ],
        "correct_answer": "L’organisation du temps",
        "created_at": datetime.now()
    },
    {
        "material_id": str(material_2_id),
        "question": "Quelle solution est proposée pour mieux étudier ?",
        "options": [
            "Créer un planning avec des objectifs simples",
            "Étudier plusieurs heures sans pause",
            "Abandonner les études",
            "Utiliser uniquement des applications"
        ],
        "correct_answer": "Créer un planning avec des objectifs simples",
        "created_at": datetime.now()
    }
]

questions_collection.insert_many(questions_2)

