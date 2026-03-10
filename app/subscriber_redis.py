import asyncio
import redis.asyncio as redis

async def main():
    r = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    pubsub = r.pubsub()
    await pubsub.subscribe("eventos_sessao")
    print("Escutando eventos de sessão...")
    async for message in pubsub.listen():

        if message["type"] == "message":
            evento = message["data"]
            print("Evento recebido:", evento)
            if "sessao_iniciada" in evento:
                print("Usuário iniciou sessão")
            if "sessao_finalizada" in evento:
                print("Usuário finalizou sessão")
asyncio.run(main())