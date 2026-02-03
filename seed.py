import random
from datetime import datetime, timedelta
from app.database import (
    materials_collection,
    questions_collection,
    users_collection,
    sessions_collection
)


# 1. DADOS: TEXTOS LONGOS (CULTURA FRANCESA) - NÍVEL B1/B2

LONG_TEXTS_DATA = [
    {
        "title": "La gastronomie et le patrimoine",
        "content": """La gastronomie française est mondialement célèbre, non seulement pour la qualité de ses plats, mais aussi pour sa diversité régionale. Chaque région possède ses propres spécialités : la choucroute en Alsace, la bouillabaisse à Marseille ou encore les crêpes en Bretagne. 
        
Mais au-delà des plats, c'est le "repas gastronomique des Français" qui a été inscrit au patrimoine culturel immatériel de l'humanité par l'UNESCO en 2010. Cette distinction ne récompense pas une recette précise, mais une pratique sociale : le fait de se réunir, de bien manger et de bien boire ensemble. Un repas traditionnel respecte un ordre précis : il commence par un apéritif, suivi d'une entrée, d'un plat principal, de fromage et enfin d'un dessert. C'est un moment de convivialité essentiel dans la vie quotidienne des Français, souvent célébré le dimanche en famille.""",
        "q1": "Qu'est-ce qui a été inscrit à l'UNESCO ?", "a1": "Le repas gastronomique des Français",
        "q2": "Quel est l'ordre correct d'un repas ?", "a2": "Apéritif, entrée, plat, fromage, dessert"
    },
    {
        "title": "Les vacances et le rythme de vie",
        "content": """En France, le droit aux vacances est sacré. Depuis 1936 et l'instauration des congés payés, les Français sont très attachés à leurs semaines de repos. Aujourd'hui, un salarié bénéficie généralement de cinq semaines de congés payés par an, sans compter les jours fériés et les RTT (Réduction du Temps de Travail).
        
L'été, particulièrement au mois d'août, l'activité économique du pays ralentit considérablement. Paris se vide de ses habitants, qui partent vers les côtes (la Côte d'Azur, la Bretagne) ou à la campagne. Ce phénomène est si marqué qu'on distingue deux types de vacanciers sur la route : les "juillettistes", qui partent en juillet, et les "aoûtiens", qui partent en août. Les embouteillages sur les autoroutes du sud sont alors inévitables et font partie du folklore estival.""",
        "q1": "Quand ont été instaurés les congés payés ?", "a1": "En 1936",
        "q2": "Qui sont les juillettistes ?", "a2": "Ceux qui partent en vacances en juillet"
    },
    {
        "title": "Le système de santé français",
        "content": """Le système de santé en France est souvent cité comme l'un des plus performants et des plus accessibles au monde. Il repose sur la Sécurité Sociale, créée en 1945, qui permet à tous les résidents d'être remboursés pour leurs frais médicaux. La célèbre "Carte Vitale", une carte à puce verte, facilite ces démarches en transmettant les informations directement aux organismes de paiement.
        
Cependant, le système fait face à des défis modernes. Le vieillissement de la population entraîne une augmentation des coûts, et certaines régions rurales souffrent de ce qu'on appelle des "déserts médicaux", c'est-à-dire un manque de médecins généralistes et de spécialistes. Pour compenser, le gouvernement encourage la télémédecine, qui permet aux patients de consulter un docteur via leur ordinateur ou smartphone.""",
        "q1": "Quelle est la couleur de la Carte Vitale ?", "a1": "Verte",
        "q2": "Qu'est-ce qu'un désert médical ?", "a2": "Une zone où il manque de médecins"
    },
    {
        "title": "L'éducation et les Grandes Écoles",
        "content": """Le système éducatif français a une particularité unique au monde : la distinction entre les Universités et les Grandes Écoles. Les universités sont ouvertes à tous les bacheliers (ceux qui ont le Baccalauréat) et sont pratiquement gratuites. Elles accueillent la majorité des étudiants.
        
À l'inverse, les Grandes Écoles (comme Polytechnique, HEC ou l'ENA) sont très sélectives. Pour y entrer, les étudiants doivent souvent passer par deux années de "classes préparatoires", qui demandent un travail intense et rigoureux, avant de passer un concours difficile. Ces écoles forment l'élite politique et économique du pays. Ce système est parfois critiqué car il favorise la reproduction sociale, les enfants de cadres ayant plus de chances d'intégrer ces écoles prestigieuses.""",
        "q1": "Quelle est la différence principale des Grandes Écoles ?", "a1": "Elles sont très sélectives",
        "q2": "Que faut-il faire avant le concours ?", "a2": "Des classes préparatoires"
    },
    {
        "title": "Paris vs La Province",
        "content": """Il existe en France une distinction culturelle et économique très forte entre Paris (et sa région, l'Île-de-France) et le reste du pays, qu'on appelle historiquement "la Province". Paris concentre les pouvoirs politiques, les sièges des grandes entreprises, les musées nationaux et les médias. C'est une ville dynamique mais stressante, où le coût de la vie et des loyers est extrêmement élevé.
        
Ces dernières années, grâce au développement du TGV (Train à Grande Vitesse) et à la généralisation du télétravail, de nombreux Parisiens ont décidé de quitter la capitale. Ils s'installent dans des villes comme Bordeaux, Lyon ou Nantes pour gagner en qualité de vie, avoir des appartements plus grands et profiter de la nature, tout en continuant parfois à travailler pour des entreprises parisiennes.""",
        "q1": "Comment appelle-t-on le reste de la France hors de Paris ?", "a1": "La Province",
        "q2": "Pourquoi les gens quittent-ils Paris ?", "a2": "Pour gagner en qualité de vie"
    },
    {
        "title": "Le cinéma : L'exception culturelle",
        "content": """La France est le berceau du cinéma, inventé par les frères Lumière à Lyon en 1895. Aujourd'hui encore, le cinéma tient une place centrale dans la culture française. La France défend ce qu'elle appelle "l'exception culturelle", un principe selon lequel la culture n'est pas une marchandise comme les autres et doit être protégée des lois du marché pur.
        
Concrètement, cela se traduit par des aides financières pour la création de films et des quotas de diffusion d'œuvres françaises à la télévision et à la radio. Le Festival de Cannes, qui a lieu chaque année en mai, est le festival de cinéma le plus célèbre au monde. Il attire les plus grandes stars internationales et récompense le meilleur film avec la prestigieuse Palme d'Or.""",
        "q1": "Qui a inventé le cinéma ?", "a1": "Les frères Lumière",
        "q2": "Quelle est la récompense suprême à Cannes ?", "a2": "La Palme d'Or"
    },
    {
        "title": "La mode et le luxe",
        "content": """Quand on parle de la France à l'étranger, on pense immédiatement à la mode. Paris est considérée comme la capitale mondiale de la mode, accueillant la "Fashion Week" deux fois par an. C'est le siège de maisons historiques comme Chanel, Dior, Louis Vuitton et Hermès. Ce secteur du luxe est vital pour l'économie française et représente une part énorme des exportations.
        
Cependant, le style des Français dans la rue est souvent différent de celui des podiums. Le "style parisien" est réputé pour être "chic décontracté". On privilégie des pièces intemporelles de bonne qualité (un trench-coat, une marinière, un jean bien coupé) plutôt que des tenues extravagantes. L'élégance à la française réside souvent dans la simplicité et le naturel.""",
        "q1": "Quelles marques sont citées ?", "a1": "Chanel, Dior, Louis Vuitton",
        "q2": "Comment est le style quotidien des Français ?", "a2": "Chic décontracté"
    },
    {
        "title": "L'écologie au quotidien",
        "content": """La conscience écologique a beaucoup progressé en France ces dernières années. Le tri des déchets est désormais obligatoire et complexe : poubelle jaune pour les emballages, verte pour le verre, marron pour les déchets alimentaires. Les supermarchés ne donnent plus de sacs plastiques, il faut apporter ses propres cabas.
        
Dans les grandes villes, la voiture est progressivement chassée au profit du vélo. Paris, par exemple, a multiplié les pistes cyclables et réduit la vitesse à 30 km/h dans la plupart des rues. Cependant, ce changement crée des tensions entre les cyclistes, les piétons et les automobilistes. De plus, le débat sur l'énergie reste vif, la France dépendant majoritairement de l'énergie nucléaire pour produire son électricité.""",
        "q1": "Quelle est la couleur de la poubelle pour le verre ?", "a1": "Verte",
        "q2": "Quelle est la source principale d'électricité ?", "a2": "L'énergie nucléaire"
    },
    {
        "title": "Les transports et la grève",
        "content": """Se déplacer en France est généralement facile grâce à un réseau de transport dense. Le TGV (Train à Grande Vitesse) permet de relier Paris à Marseille en seulement trois heures, contre plus de sept heures en voiture. À Paris, le métro est le moyen de transport le plus utilisé, bien qu'il soit souvent critiqué pour sa saleté ou ses retards.
        
Une particularité française qui surprend souvent les étrangers est la culture de la grève. Les syndicats de transports (SNCF, RATP) sont puissants et n'hésitent pas à bloquer le pays pour protester contre des réformes (retraites, salaires). Pour les usagers, ces jours de grève sont synonymes de cauchemar, obligeant beaucoup de gens à marcher ou à travailler de chez eux.""",
        "q1": "Combien de temps faut-il pour aller à Marseille en TGV ?", "a1": "Trois heures",
        "q2": "Quelle est la réaction des syndicats face aux réformes ?", "a2": "Ils font la grève"
    },
    {
        "title": "La langue française et l'Académie",
        "content": """Les Français sont très fiers et protecteurs de leur langue. L'institution chargée de veiller sur le bon usage du français est l'Académie française, fondée en 1635 par le cardinal de Richelieu. Ses membres, appelés "les Immortels", publient le dictionnaire officiel et décident des règles grammaticales.
        
L'un des grands combats actuels est la lutte contre les anglicismes. Avec la mondialisation et Internet, de nombreux mots anglais entrent dans le vocabulaire courant (marketing, week-end, challenge). L'Académie tente de proposer des équivalents français, comme "courriel" pour "email" ou "infox" pour "fake news", mais ces termes ne sont pas toujours adoptés par le grand public.""",
        "q1": "Qui a fondé l'Académie française ?", "a1": "Le cardinal de Richelieu",
        "q2": "Quel est le mot français pour 'fake news' ?", "a2": "Infox"
    },
    {
        "title": "Le sport en France",
        "content": """Le sport occupe une place importante, portée par des événements majeurs comme le Tour de France en juillet ou le tournoi de tennis de Roland-Garros. Le football reste le sport roi, surtout depuis les victoires en Coupe du Monde en 1998 et 2018.
        
Cependant, la pratique amateur évolue. De plus en plus de Français délaissent les clubs traditionnels pour des pratiques libres : course à pied (running), fitness en salle ou yoga. Les Jeux Olympiques de Paris 2024 ont également accéléré la rénovation des infrastructures sportives dans tout le pays, avec un objectif clair : faire de la France une nation plus sportive.""",
        "q1": "Quel est le sport roi en France ?", "a1": "Le football",
        "q2": "Quel événement a lieu en 2024 ?", "a2": "Les Jeux Olympiques de Paris"
    },
    {
        "title": "Le marché du travail",
        "content": """Le marché du travail français est connu pour être protecteur envers les salariés, mais aussi rigide. Le contrat standard recherché par tous est le CDI (Contrat à Durée Indéterminée), qui offre une grande sécurité de l'emploi et facilite l'accès au logement et au crédit bancaire.
        
À l'opposé, le CDD (Contrat à Durée Déterminée) est précaire. Le temps de travail légal est de 35 heures par semaine, une durée inférieure à la moyenne européenne. Si un salarié travaille plus, ces heures sont payées en heures supplémentaires ou converties en jours de repos. Le code du travail français est un livre très épais et complexe qui régit toutes ces règles.""",
        "q1": "Quel est le contrat le plus recherché ?", "a1": "Le CDI",
        "q2": "Quelle est la durée légale du travail ?", "a2": "35 heures par semaine"
    },
    {
        "title": "La famille moderne",
        "content": """La structure familiale traditionnelle (un couple marié avec deux enfants) a beaucoup évolué. Aujourd'hui, les familles monoparentales ou recomposées sont très courantes. Le nombre de mariages diminue, tandis que le PACS (Pacte Civil de Solidarité) augmente. Créé à l'origine pour les couples homosexuels, le PACS est aujourd'hui majoritairement utilisé par les hétérosexuels car il est plus souple que le mariage.
        
La France conserve l'un des taux de natalité les plus élevés d'Europe. Cela s'explique en partie par une politique familiale généreuse : allocations familiales, congés maternité et paternité, et un système de crèches publiques et d'écoles maternelles gratuites dès l'âge de trois ans.""",
        "q1": "Qu'est-ce qui remplace souvent le mariage ?", "a1": "Le PACS",
        "q2": "Pourquoi le taux de natalité est-il élevé ?", "a2": "Grâce à une politique familiale généreuse"
    },
    {
        "title": "Les animaux de compagnie",
        "content": """La France détient le record européen du nombre d'animaux domestiques. Plus d'un foyer sur deux possède un chien, un chat ou un poisson rouge. L'animal est considéré comme un membre de la famille à part entière. Le chat est désormais l'animal préféré des Français, détrônant le chien, car il s'adapte mieux à la vie en appartement en ville.
        
Cette passion a un coût : les Français dépensent des milliards d'euros chaque année pour l'alimentation et les soins vétérinaires. Malheureusement, un triste record persiste aussi : le nombre d'abandons d'animaux augmente chaque été, quand les propriétaires partent en vacances et ne peuvent pas emmener leur compagnon.""",
        "q1": "Quel est l'animal préféré actuellement ?", "a1": "Le chat",
        "q2": "Quand y a-t-il le plus d'abandons ?", "a2": "En été"
    },
    {
        "title": "La littérature et la lecture",
        "content": """Malgré la concurrence des écrans et des réseaux sociaux, la France reste un pays de lecteurs. La "Rentrée Littéraire", qui a lieu chaque année en septembre, est un phénomène unique : des centaines de nouveaux romans paraissent en même temps. Les prix littéraires, comme le Goncourt ou le Renaudot, propulsent les ventes des auteurs récompensés.
        
Le livre de poche a démocratisé la lecture en rendant les ouvrages accessibles à bas prix. De plus, la France dispose d'un réseau dense de librairies indépendantes, protégées par une loi qui interdit de vendre les livres neufs avec une réduction de plus de 5%, empêchant ainsi la concurrence déloyale des grandes surfaces ou d'Internet.""",
        "q1": "Quand a lieu la rentrée littéraire ?", "a1": "En septembre",
        "q2": "Quel prix littéraire est cité ?", "a2": "Le Goncourt"
    },
    {
        "title": "L'Histoire : La Révolution",
        "content": """L'histoire de France est longue et complexe, mais l'événement fondateur de la France moderne est sans doute la Révolution française de 1789. Elle a mis fin à la monarchie absolue et aux privilèges de la noblesse. La Prise de la Bastille, le 14 juillet 1789, est devenue la fête nationale.
        
C'est à cette époque qu'a été rédigée la Déclaration des droits de l'homme et du citoyen. La devise de la République "Liberté, Égalité, Fraternité" est née de ces bouleversements. Même si la France a connu d'autres régimes par la suite (Empires, Royautés constitutionnelles), les valeurs républicaines actuelles sont directement héritées de cette période.""",
        "q1": "Quelle est la date de la fête nationale ?", "a1": "Le 14 juillet",
        "q2": "Quelle est la devise de la France ?", "a2": "Liberté, Égalité, Fraternité"
    },
    {
        "title": "Le climat et la géographie",
        "content": """La France métropolitaine est souvent appelée "l'Hexagone" en raison de sa forme géométrique à six côtés. Malgré une taille relativement modeste par rapport à des pays comme le Brésil ou les États-Unis, elle offre une variété de paysages incroyable. On y trouve des hautes montagnes (les Alpes, les Pyrénées), des plaines agricoles, des côtes atlantiques sauvages et des plages méditerranéennes.
        
Le climat est tempéré, ce qui est idéal pour l'agriculture, premier secteur économique de nos campagnes. Cependant, le changement climatique commence à modifier la donne : les étés deviennent caniculaires, les vendanges (récolte du raisin) se font plus tôt, et les stations de ski manquent parfois de neige en hiver.""",
        "q1": "Quel est le surnom de la France ?", "a1": "L'Hexagone",
        "q2": "Quel est le problème causé par le changement climatique ?", "a2": "Les étés caniculaires"
    },
    {
        "title": "La politesse et les codes sociaux",
        "content": """Les codes de politesse en France peuvent sembler compliqués aux étrangers. La règle la plus importante est sans doute le "Bonjour". Entrer dans un magasin ou s'adresser à quelqu'un sans dire bonjour est considéré comme très impoli. De même, l'usage du "vous" (vouvoiement) est de rigueur avec les inconnus, les supérieurs hiérarchiques ou les personnes âgées.
        
La bise est une autre spécificité culturelle. Pour se saluer entre amis ou en famille, on s'embrasse sur les joues. Le nombre de bises varie selon les régions : deux à Paris, mais parfois trois ou quatre dans le sud ! C'est un rituel social incontournable qui marque l'appartenance au groupe.""",
        "q1": "Quel mot est indispensable par politesse ?", "a1": "Bonjour",
        "q2": "Quand utilise-t-on le vouvoiement ?", "a2": "Avec les inconnus ou supérieurs"
    },
    {
        "title": "Les médias et l'information",
        "content": """Le paysage médiatique français est riche mais en pleine mutation. Les grands journaux nationaux comme Le Monde, Le Figaro ou Libération existent depuis des décennies, mais ils doivent aujourd'hui se battre pour survivre face à l'information gratuite sur Internet.
        
La radio reste un média très apprécié, notamment le matin. Les Français écoutent les informations en allant au travail. La télévision publique (France Télévisions) propose des programmes culturels et d'information, tandis que les chaînes privées et les chaînes d'information en continu (comme BFM TV) sont souvent critiquées pour leur recherche du sensationnalisme et la rapidité de l'information au détriment de l'analyse.""",
        "q1": "Quels journaux sont cités ?", "a1": "Le Monde, Le Figaro, Libération",
        "q2": "Quel média est très écouté le matin ?", "a2": "La radio"
    },
    {
        "title": "Le logement en France",
        "content": """Se loger est devenu une préoccupation majeure, surtout dans les grandes villes. À Paris, les prix de l'immobilier ont atteint des sommets, obligeant les étudiants et les jeunes travailleurs à vivre dans de très petits espaces, parfois appelés "chambres de bonne" (moins de 15 mètres carrés).
        
Il existe cependant un système d'aides au logement (les APL) versées par l'État pour aider à payer le loyer. En province, la situation est différente : le rêve de beaucoup de Français reste d'acheter une maison individuelle avec un jardin. Le marché de la résidence secondaire est aussi très actif, beaucoup de citadins achetant une maison à la campagne pour les vacances et la retraite.""",
        "q1": "Comment s'appellent les petits logements à Paris ?", "a1": "Chambres de bonne",
        "q2": "Quelle aide l'État propose-t-il ?", "a2": "Les APL"
    }
]

# 2. DADOS: AUDIO TOPICS (PARA GERAR VOLUME)
AUDIO_TOPICS = [
    "L'interview d'un artiste", "Débat sur l'écologie", "La vie nocturne à Paris",
    "Les nouvelles technologies", "Apprendre le français", "Voyager en solo",
    "La cuisine végétarienne", "Le cinéma d'action", "Les jeux vidéo",
    "La santé mentale", "Le travail d'équipe", "L'histoire de Napoléon",
    "Les fêtes traditionnelles", "Le système scolaire", "La mode éthique",
    "Les transports du futur", "Vivre à la campagne", "Les réseaux sociaux",
    "La musique classique", "Les séries télévisées"
]

# 3. DADOS: PROMPTS DE PRODUÇÃO
PRODUCTION_DATA = [
    {"competence": "Production Écrite", "level": "B1", "type": "prompt", "content": "Écrivez un email pour demander des informations sur un cours."},
    {"competence": "Production Écrite", "level": "B2", "type": "prompt", "content": "Rédigez un essai sur les avantages du télétravail."},
    {"competence": "Production Écrite", "level": "A2", "type": "prompt", "content": "Racontez vos dernières vacances dans une carte postale."},
    {"competence": "Production Écrite", "level": "B1", "type": "prompt", "content": "Donnez votre avis sur l'utilisation des téléphones portables à l'école."},
    {"competence": "Production Orale", "level": "B1", "type": "prompt", "content": "Présentez-vous et parlez de vos loisirs (2 min)."},
    {"competence": "Production Orale", "level": "A2", "type": "prompt", "content": "Décrivez une personne importante dans votre vie."},
    {"competence": "Production Orale", "level": "B2", "type": "prompt", "content": "Débattez sur l'importance de l'apprentissage des langues étrangères."},
    {"competence": "Production Orale", "level": "B1", "type": "prompt", "content": "Racontez une anecdote amusante qui vous est arrivée."}
]

def run_seed():
    print("\n🚀 INICIANDO POPULAÇÃO TOTAL DO BANCO DE DADOS...\n")

    # ---------------------------------------------------------
    # PASSO 0: LIMPEZA (Cuidado em produção!)
    # ---------------------------------------------------------
    print("🧹 Limpando coleções antigas...")
    users_collection.delete_many({})
    materials_collection.delete_many({})
    questions_collection.delete_many({})
    sessions_collection.delete_many({})
    print("✅ Banco limpo.")

    # ---------------------------------------------------------
    # PASSO 1: USUÁRIOS
    # ---------------------------------------------------------
    print("👤 Inserindo usuários...")
    users = [
        {"name": "Giovana", "level": "B1", "email": "giovana@example.com"},
        {"name": "Ana", "level": "B2", "email": "ana@example.com"},
        {"name": "Lucas", "level": "A2", "email": "lucas@example.com"}
    ]
    # Adicionar +10 usuários aleatórios
    for i in range(1, 11):
        users.append({
            "name": f"Étudiant {i}",
            "level": random.choice(["A1", "A2", "B1", "B2"]),
            "email": f"student{i}@example.com"
        })

    for u in users:
        u["created_at"] = datetime.now()
    
    users_result = users_collection.insert_many(users)
    main_user_id = users_result.inserted_ids[0] # Pega o ID da Giovana
    print(f"✅ {len(users)} usuários inseridos.")

    # ---------------------------------------------------------
    # PASSO 2: TEXTOS (COMPRÉHENSION ÉCRITE)
    # ---------------------------------------------------------
    print("📖 Inserindo Textos Longos (Compréhension Écrite)...")
    count_texts = 0
    for item in LONG_TEXTS_DATA:
        mat = {
            "competence": "Compréhension Écrite",
            "level": "B1",
            "type": "text",
            "title": item["title"],
            "content": item["content"],
            "created_at": datetime.now()
        }
        mat_id = materials_collection.insert_one(mat).inserted_id
        
        # Perguntas
        qs = [
            {"material_id": str(mat_id), "question": item["q1"], "options": [item["a1"], "Non", "Peut-être", "Je ne sais pas"], "correct_answer": item["a1"], "created_at": datetime.now()},
            {"material_id": str(mat_id), "question": item["q2"], "options": [item["a2"], "Jamais", "Toujours", "Parfois"], "correct_answer": item["a2"], "created_at": datetime.now()}
        ]
        questions_collection.insert_many(qs)
        count_texts += 1
    print(f"✅ {count_texts} textos inseridos com sucesso.")

   
    # PASSO 3: ÁUDIOS (COMPRÉHENSION ORALE)
    print("🎧 Inserindo Áudios (Compréhension Orale)...")
    count_audios = 0
    for i, topic in enumerate(AUDIO_TOPICS):
        mat = {
            "competence": "Compréhension Orale",
            "level": random.choice(["A2", "B1", "B2"]),
            "type": "audio",
            "title": topic,
            "audio_url": f"https://www.youtube.com/watch?v=DEMO_{i}", # URL fictícia
            "description": f"Un enregistrement audio intéressant sur : {topic}.",
            "created_at": datetime.now()
        }
        mat_id = materials_collection.insert_one(mat).inserted_id
        
        qs = [
            {"material_id": str(mat_id), "question": f"Quel est le sujet principal ?", "options": [topic, "Le sport", "La politique", "La cuisine"], "correct_answer": topic, "created_at": datetime.now()},
            {"material_id": str(mat_id), "question": "Quel est le ton de l'audio ?", "options": ["Informatif", "Triste", "Colérique", "Ironique"], "correct_answer": "Informatif", "created_at": datetime.now()}
        ]
        questions_collection.insert_many(qs)
        count_audios += 1
    print(f"✅ {count_audios} áudios inseridos com sucesso.")

    # PASSO 4: PROMPTS DE PRODUÇÃO
    print("✍️ Inserindo Prompts de Produção...")
    for p in PRODUCTION_DATA:
        p["created_at"] = datetime.now()
    materials_collection.insert_many(PRODUCTION_DATA)
    print(f"✅ {len(PRODUCTION_DATA)} prompts inseridos.")

    # PASSO 5: SESSÕES (HISTÓRICO)
    print("📊 Gerando histórico de sessões para Giovana...")
    sessions = []
    # Cria 10 sessões nos últimos 10 dias
    for i in range(10):
        competence = random.choice(["Compréhension Orale", "Compréhension Écrite", "Production Écrite"])
        sessions.append({
            "user_id": main_user_id, # ID da Giovana
            "competence": competence,
            "session_number": i + 1,
            "start_time": datetime.now() - timedelta(days=10-i),
            "end_time": datetime.now() - timedelta(days=10-i) + timedelta(minutes=random.randint(10, 30)),
            "completed": True
        })
    sessions_collection.insert_many(sessions)
    print(f"✅ {len(sessions)} sessões inseridas.")

    print("\nBanco de Dados Pronto")

if __name__ == "__main__":
    run_seed()