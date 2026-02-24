import random
from datetime import datetime, timedelta
from faker import Faker
from app.database import (
    users_collection, 
    materials_collection, 
    questions_collection, 
    sessions_collection
)

fake = Faker(['fr_FR'])

def generate_bulk_data(n_users=10, n_materials=100, n_sessions=400):
    print(f"🚀 Iniciando população de dados para o Cycle-DELF...")

    # 1. Gerar Usuários
    user_ids = []
    levels = ['A1', 'A2', 'B1', 'B2', 'C1']
    for _ in range(n_users):
        user = {
            "name": fake.name(),
            "level": random.choice(levels),
            "email": fake.email(),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 30))
        }
        res = users_collection.insert_one(user)
        user_ids.append(res.inserted_id)

    # Listas de apoio para geração dinâmica
    temas = [
        "vos dernières vacances", "votre routine quotidienne", "une anecdote d'enfance", 
        "un voyage mémorable", "un film que vous avez aimé", "une rencontre intéressante", 
        "votre ville idéale", "une fête traditionnelle", "le sport et la santé",
        "les avantages et inconvénients du télétravail", "l'intelligence artificielle au travail",
        "la protection de l'environnement et l'écologie", "la consommation responsable",
        "l'impact des réseaux sociaux sur les jeunes", "l'égalité homme-femme",
        "le système éducatif actuel", "la liberté d'expression", "le multiculturalisme",
        "les défis de l'urbanisation", "l'éthique dans la technologie"
    ]
    
    gramatica = [
        "le passé composé", "l'imparfait", "le futur simple", "le conditionnel présent", 
        "les pronoms relatifs simples (qui, que, dont)", "le comparatif et le superlatif",
        "le subjonctif présent et passé", "le conditionnel passé (regret/reproche)",
        "le plus-que-parfait", "le gérondif (manière/cause)", "la voix passive",
        "les pronoms relatifs composés (auquel, desquels)", "les articulateurs logiques (bien que, malgré, toutefois)",
        "la double prononciation", "le futur antérieur", "l'expression du but e de la peur"
    ]
    
    contextos = [
        "un email formel", "un article de blog", "une lettre amicale", "un message sur un forum",
        "un essai argumentatif", "une lettre de motivation", "un compte-rendu de réunion", 
        "une critique de livre ou de film", "une lettre de réclamation", "un discours officiel",
        "un éditorial de journal", "une note de synthèse"
    ]

    all_materials = []
    
    # 2. Loop de Geração de Materiais
    for _ in range(n_materials):
        comp = random.choice(["Compréhension Écrite", "Compréhension Orale", "Production Écrite", "Production Orale"])
        level = random.choice(levels)
        
        material = {
            "competence": comp,
            "level": level,
            "created_at": datetime.now(),
            "location": {
                "type": "Point",
                "coordinates": [float(fake.longitude()), float(fake.latitude())]
            }
        }

        if "Production" in comp:
            t = random.choice(temas)
            g = random.sample(gramatica, k=random.randint(1, 2)) # Pega 1 ou 2 gramáticas
            c = random.choice(contextos)
            
            # Monta o enunciado dinamicamente
            instrucao = f"Rédigez {c} sur {t} en utilisant particulièrement {', '.join(g)}."
            if comp == "Production Orale":
                instrucao = f"Présentation Orale: Parlez de {t}. Consigne: Utilisez {', '.join(g)}."

            material.update({
                "type": "prompt",
                "title": f"Sujet {level} - {comp}",
                "content": instrucao
            })
        
        elif comp == "Compréhension Orale":
            material.update({
                "type": "audio",
                "title": fake.sentence(nb_words=4),
                "audio_url": f"https://www.youtube.com/watch?v={fake.bothify('??##??##')}",
                "content": fake.text(max_nb_chars=200)
            })
        else: # Compréhension Écrite
            material.update({
                "type": "text",
                "title": fake.sentence(nb_words=4),
                "content": fake.text(max_nb_chars=800)
            })
        
        all_materials.append(material)

    # InsertMany de Materiais (Requisito da Disciplina)
    materials_res = materials_collection.insert_many(all_materials)
    inserted_ids = materials_res.inserted_ids

    # 3. Gerar Questões (apenas para Compreensão)
    all_questions = []
    for i, m_id in enumerate(inserted_ids):
        if "Compréhension" in all_materials[i]["competence"]:
            for _ in range(3):
                all_questions.append({
                    "material_id": str(m_id),
                    "question": fake.sentence() + " ?",
                    "options": [fake.word(), fake.word(), fake.word(), "Réponse Correcte"],
                    "correct_answer": "Réponse Correcte",
                    "created_at": datetime.now()
                })
    
    if all_questions:
        questions_collection.insert_many(all_questions)

    # 4. Gerar Sessões para o Analytics
    all_sessions = []
    for _ in range(n_sessions):
        start = datetime.now() - timedelta(days=random.randint(0, 30))
        all_sessions.append({
            "user_id": str(random.choice(user_ids)),
            "competence": random.choice(["Compréhension Écrite", "Compréhension Orale", "Production Écrite", "Production Orale"]),
            "score": random.randint(30, 100),
            "duration_minutes": random.randint(5, 60),
            "start_time": start,
            "completed": True
        })
    
    sessions_collection.insert_many(all_sessions)
    print(f"✅ População concluída com sucesso!")

if __name__ == "__main__":
    generate_bulk_data()