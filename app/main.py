from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from bson import ObjectId
from app.database import db_connection, connect_to_nosql, close_nosql_connections
from app.funcionalidade import (start_session,finish_session)
from pymongo import ASCENDING, TEXT, GEOSPHERE 
from typing import Optional 
import random 
import time
from contextlib import asynccontextmanager

# ---------------------------------------------------------
# GERENCIAMENTO DE CICLO DE VIDA (CONEXÃO E ÍNDICES)
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_nosql()    
    try:
        await db_connection.users.create_index([("name", ASCENDING)], unique=True)
        await db_connection.users.create_index([("level", ASCENDING)])
        await db_connection.users.create_index([("location", GEOSPHERE)])
        await db_connection.materials.create_index([
            ("title", TEXT), 
            ("content", TEXT),
            ("competence", TEXT)
        ], name="busca_texto_global")
        print("✅ Índices NoSQL configurados!")
    except Exception as e:
        print(f"⚠️ Erro ao criar índices: {e}")
        
    yield
    await close_nosql_connections()

app = FastAPI(title="Cycle DELFS", lifespan=lifespan)

# --- CONFIGURAÇÃO DE CORS (O que estava faltando) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer front-end (Streamlit) acesse
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# ROTAS PARA O DASHBOARD (Fix 404)
# ---------------------------------------------------------

@app.get("/users")
async def list_users():
    users = []
    cursor = db_connection.users.find()
    for user in await cursor.to_list(length=100):
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.get("/materials")
async def list_materials():
    materials = []
    cursor = db_connection.materials.find()
    for m in await cursor.to_list(length=100):
        m["_id"] = str(m["_id"])
        materials.append(m)
    return materials

@app.get("/analytics/top-users")
async def top_users():
    # Retorna uma lista vazia se o banco estiver limpo, em vez de dar erro
    pipeline = [{"$group": {"_id": "$user_id", "total": {"$sum": 1}}}, {"$limit": 5}]
    result = await db_connection.sessions.aggregate(pipeline).to_list(length=5)
    return result

@app.get("/analytics/monthly-progress/{user_id}")
async def monthly_progress(user_id: str):
    # Rota que o Dashboard estava pedindo no seu log
    return [{"mes": "Março", "progresso": 0}]

# ---------------------------------------------------------
# ROTAS DE USUÁRIOS 
# ---------------------------------------------------------

@app.post("/users")
async def create_user(user: dict):
    if "level" not in user:
        user["level"] = "A1"
    if "location" not in user:
        user["location"] = {
            "type": "Point",
            "coordinates": [random.uniform(-46.8, -46.3), random.uniform(-23.7, -23.4)]
        }
    
    user["created_at"] = datetime.now()
    result = await db_connection.users.insert_one(user)
    return {"message": "Usuário criado", "id": str(result.inserted_id)}

@app.get("/users")
async def list_users():
    users = []
    cursor = db_connection.users.find()
    for user in await cursor.to_list(length=100):
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.get("/users/filter")
async def filter_users(level: Optional[str] = None):
    query = {}
    if level:
        query["level"] = level.strip()
    
    cursor = db_connection.users.find(query)
    users = await cursor.to_list(length=100)
    for u in users:
        u["_id"] = str(u["_id"])
    return users

@app.get("/users/nearby")
async def get_nearby_users(lat: float, lon: float, radius_km: float = 10):
    query = {
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": radius_km * 1000
            }
        }
    }
    cursor = db_connection.users.find(query)
    users = await cursor.to_list(length=100)
    for u in users:
        u["_id"] = str(u["_id"])
    return users

@app.get("/analytics/top-users")
async def top_users():
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "total_sessions": {"$sum": 1}
            }
        },
        {"$sort": {"total_sessions": -1}},
        {"$limit": 5}
    ]

    result = await db_connection.sessions.aggregate(pipeline).to_list(length=5)

    users = []
    for r in result:
        user = await db_connection.users.find_one({"_id": ObjectId(r["_id"])})
        if user:
            users.append({
                "name": user["name"],
                "sessions": r["total_sessions"]
            })

    return users

# ---------------------------------------------------------
# ROTAS DE MATERIAIS
# ---------------------------------------------------------

@app.get("/materials")
async def list_materials():
    """Retorna todos os materiais para o Dashboard"""
    materials = []
    cursor = db_connection.materials.find()
    for m in await cursor.to_list(length=100):
        m["_id"] = str(m["_id"])
        materials.append(m)
    return materials

@app.get("/materials/search")
async def search_materials(q: str):
    query = {"$text": {"$search": q.strip()}}
    cursor = db_connection.materials.find(query)
    materials = await cursor.to_list(length=50)
    for m in materials:
        m["_id"] = str(m["_id"])
    return materials
# ---------------------------------------------------------
# SESSIONS E CICLO (REDIS + MONGO)
# ---------------------------------------------------------

@app.post("/sessions/start/{user_id}")
async def start_user_session(user_id: str):
    try:
        return await start_session(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sessao/iniciar/{user_id}")
async def iniciar_modulo_redis(user_id: str, modulo: str):
    chave = f"sessao_ativa:{user_id}"
    dados_sessao = {
        "modulo": modulo,
        "inicio": str(time.time()),
        "status": "em_progresso"
    }
    await db_connection.redis.hset(chave, mapping=dados_sessao)
    await db_connection.redis.expire(chave, 1200)

    # PUBLISH 
    await db_connection.redis.publish(
        "eventos_sessao",
        f"sessao_iniciada:{user_id}:{modulo}"
    )
    return {"msg": f"Ciclo de {modulo} iniciado no Redis!"}

@app.post("/sessao/finalizar/{user_id}")
async def finalizar_sessao_redis(user_id: str):
    hoje = datetime.now().timetuple().tm_yday
    chave_streak = f"streak:{datetime.now().year}:{user_id}"

    #BITMAP
    await db_connection.redis.setbit(chave_streak, hoje, 1)
    dias_ativos = await db_connection.redis.bitcount(chave_streak)
    # PUBLISH 
    await db_connection.redis.publish(
        "eventos_sessao",
        f"sessao_finalizada:{user_id}"
    )

    return {"msg": "Sessão concluída!", "dias_totais_no_ano": dias_ativos}
# ---------------------------------------------------------
# DATA ANALYTICS (AGGREGATION)
# ---------------------------------------------------------
@app.get("/analytics/monthly-progress/{user_id}")
async def monthly_progress(user_id: str):
    """Gera dados para o gráfico de evolução mensal (Fix para Erro 404)"""
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": {"$month": "$data_fim"}, 
            "total": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = await db_connection.sessions.aggregate(pipeline).to_list(length=12)
    # Mapeia números de meses para nomes
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    return [{"mes": meses[r["_id"]-1], "progresso": r["total"]} for r in result]

@app.get("/analytics/activity-by-competence/{user_id}")
async def activity_by_competence(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": "$competence",
            "sessions": {"$sum": 1},
            "avg_score": {"$avg": "$score"}
        }},
        {"$sort": {"sessions": -1}}
    ]
    return await db_connection.sessions.aggregate(pipeline).to_list(length=20)

# ---------------------------------------------------------
# REDIS AVANÇADO (BLOOM & HLL)
# ---------------------------------------------------------
@app.get("/material/proximo/{user_id}")
async def pegar_material(user_id: str):
    # Busca qualquer material se não achar de 'escrita' para evitar 404 travado
    material = await db_connection.materials.find_one({"tipo": "escrita"})
    if not material:
        material = await db_connection.materials.find_one()
    
    if not material:
        raise HTTPException(status_code=404, detail="Nenhum material cadastrado no MongoDB.")
        
    material_id = str(material["_id"])    
    try:
        visto = await db_connection.redis.sismember(f"vistos:{user_id}", material_id)
        
        if visto:
            return {
                "msg": "O Bloom Filter detectou que você já viu este material!",
                "status": "visto",
                "material_id": material_id
            }
        
        await db_connection.redis.sadd(f"vistos:{user_id}", material_id)
        await db_connection.redis.expire(f"vistos:{user_id}", 3600) 
        
    except Exception as e:
        print(f"Erro no filtro de vistos: {e}")

@app.post("/vocabulario/adicionar/{user_id}")
async def adicionar_palavras(user_id: str, palavras: list[str]):
    # HyperLogLog para estimativa de vocabulário único
    chave_hll = f"vocab_estimado:{user_id}"
    await db_connection.redis.pfadd(chave_hll, *palavras) 
    total_estimado = await db_connection.redis.pfcount(chave_hll)
    return {"total_palavras_vistas_aproximadamente": total_estimado}

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@app.get("/buscar/semantica")
async def busca_semantica(pergunta: str):
    query_vector = model.encode(pergunta).tolist()
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "index_vetor", 
                "path": "embedding_vector",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 3
            }
        },
        {
            # ISSO AQUI RESOLVE O ERRO:
            "$project": {
                "_id": 0,  # Diz para o Mongo NÃO trazer o ID
                "title": 1,
                "content": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    cursor = db_connection.materials.aggregate(pipeline)
    return await cursor.to_list(3)