from api.core.redis_client import get_client
from api.exceptions import ServerErrorException, NotFoundException

class WordleService:
    def __init__(self):
        pass

    async def ping_redis(self):
        try:
            client = await get_client()
            db_size = await client.dbsize()
            return {"status": "ok", "redis_keys_count": db_size}
        except Exception as e:
            raise ServerErrorException(f"Failed to connect to Redis: {str(e)}")

    async def get_test_data(self, key: str):
        client = await get_client()
        val = await client.get(key)
        if not val:
            raise NotFoundException(f"Key '{key}' not found in Redis.")
        return val.decode("utf-8")

service = WordleService()
