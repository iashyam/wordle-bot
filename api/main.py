from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware
from api.exceptions import register_exception_handlers
from api.routes import router as api_router
import api.core.redis_client as redis_client
from api.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Wordle Bot API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Request: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Completed in {process_time:.2f}ms"
    )
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to match your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Wordle Bot API...")
    await redis_client.test_redis()


@app.get("/")
def read_root():
    return {"Hello": "Wordle Bot"}
