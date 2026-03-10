import asyncio
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from app.database import db_connection, connect_to_nosql, close_nosql_connections

load_dotenv()


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

async def gerar_embeddings():
    await connect_to_nosql()
    
    print("🧠 Iniciando a geração de vetores (isso pode levar alguns minutos)...")
    
    materiais = await db_connection.materials.find().to_list(None)
    
    for m in materiais:
        # Criamos uma "identidade" para o texto
        texto = f"{m.get('title', '')} {m.get('content', '')}"
        # O modelo transforma o texto em um vetor (lista de floats)
        vetor = model.encode(texto, normalize_embeddings=True).tolist()
        # Atualiza o documento no Mongo com o novo campo 'embedding_vector'
        await db_connection.materials.update_one(
            {'_id': m['_id']},
            {'$set': {'embedding_vector': vetor}}
        )
        print(f"✅ Vetor gerado para: {m.get('title', 'Sem título')}")

    print("\n🚀 Todos os materiais agora têm 'inteligência vetorial'!")
    await close_nosql_connections()

if __name__ == "__main__":
    asyncio.run(gerar_embeddings())