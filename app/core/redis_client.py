from dotenv import load_dotenv
from redis.asyncio import Redis
import os
import asyncio
load_dotenv()


redis_uri = os.getenv("REDIS_URI")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")
redis_dbname = "wordle-bot"

redis_client = Redis(host=redis_uri, port=redis_port, password=redis_password, db=0)


async def get_client():
    return redis_client

async def set_key(key, value):
    redis_client.set(key, value)

async def get_key(key):
    return redis_client.get(key)

async def test_redis():
    await redis_client.set("name", "bond")
    print(str(await redis_client.get("name")))

if __name__ == "__main__":
    asyncio.run(test_redis())

