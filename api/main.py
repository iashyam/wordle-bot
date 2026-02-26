import api.core.redis_client as redis_client
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await redis_client.test_redis()


@app.get("/")
def read_root():
    return {"Hello": "World"}
