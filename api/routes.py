from fastapi import APIRouter
from api.services import service
from api.models import StartSessionRequest, PredictRequest, CloseRequest

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

@router.post("/start")
async def start_session(request: StartSessionRequest):
    return await service.start_session(request.session_id)

@router.post("/predict_next_word")
async def predict_next_word(request: PredictRequest):
    return await service.predict_next_word(request.session_id, request.guess, request.pattern)

@router.post("/close")
async def close_session(request: CloseRequest):
    return await service.close_session(request.session_id)
