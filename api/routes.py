from fastapi import APIRouter
from api.services import service
from pydantic import BaseModel

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/redis-status")
async def get_redis_status():
    result = await service.ping_redis()
    return result

@router.get("/data/{key}")
async def get_data(key: str):
    val = await service.get_test_data(key)
    return {"key": key, "value": val}
