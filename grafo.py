import os
import asyncio
from dotenv import load_dotenv
from neo4j import GraphDatabase
from app.database import db_connection, connect_to_nosql, close_nosql_connections

load_dotenv()

# Pegando as variáveis EXATAS do seu .env
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PWD = os.getenv("NEO4J_PASSWORD")

async def importar_dados():
    await connect_to_nosql()
    
    # Criando o driver com as variáveis que acabamos de puxar
    driver = GraphDatabase.driver(URI, auth=(USER, PWD))
    
    try:
        print(f"🚀 Tentando conectar no Neo4j com o usuário: {USER}...")
        driver.verify_connectivity() # Testa a senha antes de tudo
        
        usuarios = await db_connection.users.find().to_list(100)
        materiais = await db_connection.materials.find().to_list(100)

        with driver.session() as session:
            # Criar Nós
            for u in usuarios:
                session.run("MERGE (u:Usuario {id: $id}) SET u.nome = $nome", id=str(u["_id"]), nome=u["name"])
            for m in materiais:
                session.run("MERGE (m:Material {id: $id}) SET m.titulo = $titulo", id=str(m["_id"]), titulo=m.get("title", "Sem Título"))
            
            # Relacionamento de Teste (Étudiant 6 -> Primeiro Material)
            if usuarios:
                session.run("""
                    MATCH (u:Usuario {nome: 'Étudiant 6'}), (m:Material)
                    WITH u, m LIMIT 1
                    MERGE (u)-[:ESTUDOU {data: datetime()}]->(m)
                """)

        print("✅ SUCESSO! Vá ao console do Aura e dê o Play no MATCH (n) RETURN n")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.close()
        await close_nosql_connections()

if __name__ == "__main__":
    asyncio.run(importar_dados())