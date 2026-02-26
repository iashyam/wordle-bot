import app.core.redis_client
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await app.core.redis_client.test_redis()
