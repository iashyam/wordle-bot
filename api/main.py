from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.exceptions import register_exception_handlers
from api.routes import router as api_router
import api.core.redis_client as redis_client

app = FastAPI(title="Wordle Bot API")

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
    await redis_client.test_redis()


@app.get("/")
def read_root():
    return {"Hello": "Wordle Bot"}
